# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 19:59:58 2013

@author: pilatus
"""


def recPrint(root, offs):
    offs = offs + "   "
    print offs, root.tag
    for el in root: 
        if len(list(el))>1:
            recPrint(el, offs)
        else: print el.tag

def setup(dump_filename):
    """ return the dump root as ElementTree.Element """
    import xml.etree.ElementTree as ET
    
    dump = ET.parse(dump_filename)        
    return dump.getroot()