#!/bin/bash
set -x
# first arg is a folder
#for D1 in `find $1 -type d -name "DUT*"`
for D1 in `find $1 -type d -name "DUT*"`
 do
  echo "directory is $D1"
  notnavcsv=$(find $D1 -name rf-on-off.csv -o -name starts.csv -o -name corr-on-off.csv)
  if [[ ! -z  $notnavcsv ]]; then
   echo "running not nav test on $notnavcsv"
   for file in $notnavcsv
     do
       PYTHONPATH=. python-plotting/gtt_upload.py -m -n -p $file &
       done
   fi
   navcsv=$(find $D1 -name nav.csv)
   if [[ ! -z $navcsv ]]; then
     echo "running nav test on $navcsv"
     for file in $navcsv
       do
       PYTHONPATH=. python-plotting/gtt_upload.py -m -p $file &
       done
   fi
done
# for each subfolder, traverse down tree until a csv file is found

# if a csv file is found in the rf-on-off, starts, or corr-on-off list, run script against that csv with the -n arg

# if none of those CSV files are found but a nav.csv exists, run script against the nav.csv
