#!/bin/bash

#export H="/media/aschumilin/MYLINUXLIVE/AIFB/Wikinews/"
#export M="/dev/shm/wikinews/"
# example article :
# /dev/shm/wikinews/articles_cleaned/86383-Al_Sharpton_speaks_out_on_race,_rights_and_w

mkdir /dev/shm/wikinews

# 2: extract the pages
cp /media/aschumilin/MYLINUXLIVE/AIFB/datasets/en/wikinews-pages.tar.gz /dev/shm/wikinews/
cd /dev/shm/wikinews/ # ohne gehts nicht
tar -zxf wikinews-pages.tar.gz

mv /dev/shm/wikinews/dev/shm/wikinews/* /dev/shm/wikinews/

# 2.1: cleanup
rm -fR /dev/shm/wikinews/dev/
rm /dev/shm/wikinews/wikinews-pages.tar.gz

# 3: make a target dir for good pages
mkdir /dev/shm/wikinews/articles_cleaned

# 4: execute filter2
python /media/aschumilin/MYLINUXLIVE/AIFB/Wikinews/parser/filter2.py

# 5: manual cleaning of bad pages
rm /dev/shm/wikinews/articles_cleaned/*Main_Page*
rm /dev/shm/wikinews/articles_cleaned/*-Colleges_offering_admission_to_displaced_New
rm /dev/shm/wikinews/articles_cleaned/54162-2006_U.S._Congressional_Elections
rm /dev/shm/wikinews/articles_cleaned/180311-2010_UK_general_election_results
rm /dev/shm/wikinews/articles_cleaned/8636-Results_of_2005_United_Kingdom_General_Electi
rm /dev/shm/wikinews/articles_cleaned/*-Australia-200*
rm /dev/shm/wikinews/articles_cleaned/*News_briefs*
rm /dev/shm/wikinews/articles_cleaned/*Wikinews_Shorts*
rm /dev/shm/wikinews/articles_cleaned/*-Crosswords-*

# these contain broken wiki markup syntax
rm /dev/shm/wikinews/articles_cleaned/207413-* 
rm /dev/shm/wikinews/articles_cleaned/562833-*




# 6: extract candidate entities from each article (entities & lang-links)
python /media/aschumilin/MYLINUXLIVE/AIFB/Wikinews/parser/filter3.py

#7: separate lang-links from entities
python /media/aschumilin/MYLINUXLIVE/AIFB/Wikinews/parser/filter4.py

#8: remove articles containing less than (<) X entity mentions (now, threshold is 3)
python /media/aschumilin/MYLINUXLIVE/AIFB/Wikinews/parser/filter5.py

#9: build tensor
python /media/aschumilin/MYLINUXLIVE/AIFB/Wikinews/tensor/make.py


echo "done"
