# rescal_sparse.py - python script to compute the RESCAL tensor factorization
# Author: Maximilian Nickel <nickel@dbs.ifi.lmu.de>

import logging
import time
import numpy as np
from numpy import dot, zeros, array, eye, diag, ones
from numpy.linalg import norm, inv, svd
from scipy.sparse import csr_matrix, coo_matrix, issparse
from scipy.sparse.linalg import eigsh
from numpy.random import rand
from operator import isSequenceType

__version__ = "0.3"
__all__ = ['rescal']

__DEF_MAXITER = 500
__DEF_INIT = 'nvecs'
__DEF_PROJ = True
__DEF_CONV = 1e-4
__DEF_LMBDA = 0
__DEF_ATTR = []


_log = logging.getLogger('RESCAL')


def rescal(X, rank, **kwargs):
    """
    Sparse RESCAL

    Factors a _sparse_ three-way tensor X such that each frontal slice
    X_k = A * R_k * A.T. The frontal slices of a tensor are
    _sparse_ N x N matrices that correspond to the adjecency matrices
    of the relational graph for a particular relation.

    For a full description of the algorithm see:
    [1] Maximilian Nickel, Volker Tresp, Hans-Peter-Kriegel,
        "A Three-Way Model for Collective Learning on Multi-Relational Data",
        ICML 2011, Bellevue, WA, USA

    [2] Maximilian Nickel, Volker Tresp, Hans-Peter-Kriegel,
        "Factorizing YAGO: Scalable Machine Learning for Linked Data"
        WWW 2012, Lyon, France

    Parameters
    ----------
    X : list
        List of frontal slices X_k of the tensor X.
        The shape of each X_k is ('N', 'N').
        X_k's are expected to be instances of scipy.sparse.csr_matrix
    rank : int
        Rank of the factorization
    lmbdaA : float, optional
        Regularization parameter for A factor matrix. 0 by default
    lmbdaR : float, optional
        Regularization parameter for R_k factor matrices. 0 by default
    lmbdaV : float, optional
        Regularization parameter for V_l factor matrices. 0 by default
    attr : list, optional
        List of sparse ('N', 'L_l') attribute matrices. 'L_l' may be different
        for each attribute
    init : string, optional
        Initialization method of the factor matrices. 'nvecs' (default)
        initializes A based on the eigenvectors of X. 'random' initializes
        the factor matrices randomly.
    aggregate : boolean, optional
        Perform automatic aggregation on relations and attributes.
        False by default
    fit_method : string, optional
        Method to compute convergence criterion. 'full' (default) computes
        on whole tensor. Exact but not applicable to large-scale data due to
        memory requirements. 'samples' computes fit on sample of X. Sample
        indices must be set with parameter 'samples'
    maxIter : int, optional
        Maximium number of iterations of the ALS algorithm. 500 by default.
    conv : float, optional
        Stop when residual of factorization is less than conv. 1e-5 by default

    Returns
    -------
    A : ndarray
        array of shape ('N', 'rank') corresponding to the factor matrix A
    R : list
        list of 'M' arrays of shape ('rank', 'rank') corresponding to the
        factor matrices R_k
    f : float
        function value of the factorization
    iter : int
        number of iterations until convergence
    exectimes : ndarray
        execution times to compute the updates in each iteration
    """

    # ------------ init options ----------------------------------------------
    ainit = kwargs.pop('init', __DEF_INIT)
    maxIter = kwargs.pop('maxIter', __DEF_MAXITER)
    conv = kwargs.pop('conv', __DEF_CONV)
    lmbdaA = kwargs.pop('lambda_A', __DEF_LMBDA)
    lmbdaR = kwargs.pop('lambda_R', __DEF_LMBDA)
    lmbdaV = kwargs.pop('lambda_V', __DEF_LMBDA)
    P = kwargs.pop('attr', __DEF_ATTR)
    dtype = kwargs.pop('dtype', np.float32)
    normalize = kwargs.pop('normalize', False)
    callback = kwargs.pop('callback', None)

    # ------------- check input ----------------------------------------------
    if not len(kwargs) == 0:
        raise ValueError('Unknown keywords (%s)' % (kwargs.keys()))

    for i in xrange(len(X)):
        if not issparse(X[i]):
            raise ValueError('X[%d] is not a sparse matrix' % i)

    sz = X[0].shape
    n = sz[0]
    k = len(X)

    _log.debug('[Config] rank: %d | maxIter: %d | conv: %7.1e | lmbda: %7.1e' % (rank,
        maxIter, conv, lmbdaA))
    _log.debug('[Config] dtype: %s / %s' % (dtype, X[0].dtype))

    # ------- convert X and P to CSR -----------------------------------------------
    for i in xrange(k):
        #assert (X[i].data == 1).all()
        X[i] = X[i].tocsr()
        X[i].sort_indices()
    for i in xrange(len(P)):
        P[i] = P[i].tocsr()
        P[i].sort_indices()

    if len(P) > 0:
        n_cols = sum([Pi.shape[1] for Pi in P])
        n_nnz = sum([Pi.nnz for Pi in P])
        L = coo_matrix((X[0].shape[0], n_cols))
        print L.shape, n_nnz
        offset = 0
        for Pi in P:
            L.data = np.append(L.data, Pi.data)
            L.row = np.append(L.row, Pi.tocoo().row)
            L.col = np.append(L.col, Pi.tocoo().col + offset)
            offset += Pi.shape[1]
            print Pi.shape
        L = L.tocsr()
        assert L.nnz == n_nnz
        P = [L]

    # ---------- initialize A ------------------------------------------------
    _log.debug('Initializing A')
    if ainit == 'random':
        A = array(rand(n, rank), dtype=dtype)
    elif ainit == 'nvecs':
        S = csr_matrix((n, n), dtype=dtype)
        for i in xrange(k):
            S = S + X[i]
            S = S + X[i].T
        _log.debug('nvecs initializer: shape %s, nnz %d' % (str(S.shape), S.nnz))
        _, A = eigsh(csr_matrix(S, dtype=dtype, shape=(n, n)), rank, which='LA', ncv=5 * rank)
        A = array(A, dtype=dtype)
    else:
        raise 'Unknown init option ("%s")' % ainit

    # ------- initialize R and Z ---------------------------------------------
    R, nrm_R = __updateR(X, A, lmbdaR, normalize)
    Z, nrm_Z = __updateZ(A, P, lmbdaV, normalize)

    #  ------ compute factorization ------------------------------------------
    fit = fitchange = fitold = f = 0
    exectimes = []
    for iter in xrange(maxIter):
        tic = time.time()
        #tic = time.clock()
        fitold = fit
        A, nrm_A = __updateA(X, A, R, P, Z, lmbdaA, normalize)
        R, nrm_R = __updateR(X, A, lmbdaR, normalize)
        Z, nrm_Z = __updateZ(A, P, lmbdaV, normalize)

        # compute fit value
        fit = __compute_fit(X, A, R, P, Z, lmbdaA, lmbdaR, lmbdaV, nrm_R, nrm_Z)

        fitchange = abs(fitold - fit)

        #toc = time.clock()
        toc = time.time()
        exectimes.append(toc - tic)

        _log.debug('[%3d] fit: %0.5f | delta: %7.1e | secs: %.5f' % (iter,
            fit, fitchange, exectimes[-1]))
        if iter > 0 and fitchange < conv:
            break
        if callback != None:
            callback(iter, A, R)
    #A = A * nrm_A
    #R = [Rn * nrm_R for Rn in R]
    return A, R, f, iter + 1, array(exectimes)


# ------------------ Update A ------------------------------------------------
def __updateA(X, A, R, P, Z, lmbdaA, normalize):
    """Update step for A"""
    _log.debug('Updating A')
    n, rank = A.shape
    F = zeros((n, rank), dtype=A.dtype)
    E = zeros((rank, rank), dtype=A.dtype)
    nrm = ones(rank)

    AtA = dot(A.T, A)

    for i in range(len(X)):
        F += X[i].dot(dot(A, R[i].T)) + X[i].T.dot(dot(A, R[i]))
        E += dot(R[i], dot(AtA, R[i].T)) + dot(R[i].T, dot(AtA, R[i]))

    # regularization
    I = lmbdaA ** 2 * eye(rank, dtype=A.dtype)

    # attributes
    for i in range(len(Z)):
        F += P[i].dot(Z[i].T)
        E += dot(Z[i], Z[i].T)

    # finally compute update for A
    A = dot(F, inv(I + E))
    if normalize:
        nrm = np.sqrt((A ** 2).sum(axis=0))
        A = A / nrm
    _log.debug('Updated A lambda_A:%f, dtype:%s' % (lmbdaA, A.dtype))
    return A, nrm


# ------------------ Update R ------------------------------------------------
def __updateR(X, A, lmbdaR, normalize):
    _log.debug('Updating R (SVD) lambda R: %s' % str(lmbdaR))
    U, S, Vt = svd(A, full_matrices=False)
    nrm = 1.0
    S = S / (S ** 2 + lmbdaR ** 2)
    _A = dot(Vt.T, dot(diag(S), U.T))
    R = []
    for i in xrange(len(X)):
        Rn = dot(_A, X[i].dot(_A.T))
        R.append(Rn)
    if normalize:
        nrm = np.sqrt(sum([sum(Rn ** 2) for Rn in R]))
        R = [Rn / nrm for Rn in R]
    return R, nrm


# ------------------ Update Z ------------------------------------------------
def __updateZ(A, P, lmbdaZ, normalize):
    Z = []
    if len(P) == 0:
        return Z, None
    _log.debug('Updating Z (SVD, %d)' % len(P))
    U, S, Vt = svd(A, full_matrices=False)
    S = S / (S ** 2 + lmbdaZ)
    _A = dot(Vt.T, dot(diag(S), U.T)).T
    nrm = [ones(A.shape[1]) for _ in xrange(len(P))]
    for i in xrange(len(P)):
        Zn = P[i].T.dot(_A).T
        #print Zn.shape
        if normalize:
            nrm[i] = np.sqrt((Zn ** 2).sum(axis=1))
            Zn = (Zn.T / nrm[i]).T
        #    print Zn.shape
        Z.append(Zn)
    return Z, nrm


def __compute_fit(X, A, R, P, Z, lmbdaA, lmbdaR, lmbdaZ, nrm_R, nrm_Z):
    """Compute fit for full slices"""
    f = 0
    # precompute norms of X
    normX = [sum(M.data ** 2) for M in X]
    sumNorm = sum(normX)
    #sumNorm += sum([Pi.nnz for Pi in P])

    for i in xrange(len(X)):
        ARAt = dot(A, dot(R[i] * nrm_R, A.T))
        f += norm(X[i] - ARAt) ** 2
        #f += normX[i] + norm(ARAt)**2 - 2*dot(Xflat[i], ARAt.flatten()) + lmbda*(R[i].flatten()**2).sum()
    #print 1 - f / (sumNorm - norm(P)**2)

    #for i in xrange(len(P)):
    #    print 1-(norm(P - dot(A, Z))**2)/(norm(P)**2)
    #    f += norm(P[i] - dot(A, (nrm_Z[i] * Z[i].T).T)) ** 2
    return 1 - f / sumNorm
