#!/bin/bash

#export H="/media/MYLINUXLIVE/AIFB/Wikinews/"
#export M="/dev/shm/wikinews/"

mkdir /dev/shm/wikinews

# 2: extract the pages
cp /media/MYLINUXLIVE/AIFB/datasets/en/wikinews-pages.tar.gz /dev/shm/wikinews/
cd /dev/shm/wikinews/ # ohne gehts nicht
tar -zxvf wikinews-pages.tar.gz

mv /dev/shm/wikinews/dev/shm/wikinews/* /dev/shm/wikinews/

# 2.1: cleanup
rm -fR /dev/shm/wikinews/dev/
rm /dev/shm/wikinews/wikinews-pages.tar.gz

# 3: make a target dir for good pages
mkdir /dev/shm/wikinews/articles_cleaned

# 4: execute filter2
python /media/MYLINUXLIVE/AIFB/Wikinews/parser/filter2.py

# #5: manual cleaning
rm /dev/shm/wikinews/articles_cleaned/3-Main_Page
rm /dev/shm/wikinews/articles_cleaned/118215-Main_Page_Lite
rm /dev/shm/wikinews/articles_cleaned/*-Colleges_offering_admission_to_displaced_New
rm /dev/shm/wikinews/articles_cleaned/54162-2006_U.S._Congressional_Elections
rm /dev/shm/wikinews/articles_cleaned/180311-2010_UK_general_election_results
rm /dev/shm/wikinews/articles_cleaned/8636-Results_of_2005_United_Kingdom_General_Electi
rm /dev/shm/wikinews/articles_cleaned/*-Australia-200*


# example article :
# /dev/shm/wikinews/articles_cleaned/86383-Al_Sharpton_speaks_out_on_race,_rights_and_w



