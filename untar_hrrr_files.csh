#!/bin/csh

# Brian Blaylock
# Untar hrrr files in the Horel archive for an entire month (or change the days for a set of days)
# and moves them to the directory the script is run in.

# I suppose if you are some random user to stumble accross our HRRR archive you can use 
# a wget get comand to download the tarred file from the following URL:
# https://api.mesowest.utah.edu/archive/20150619/models/hrrr/
# with the YYYYMMDD modified for each day you want to grab. Best of luck!

echo ''
set year = '2015'
set month = '07'

foreach day ( 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 23 24 25 26 27 28 29 30 31 )
   echo grabbing this day {$year}{$month}{$day}
   
   ## Add wget command here if you need to download the models.tar.gz file
   # wget https://api.mesowest.utah.edu/archive/{$year}{$month}{$day}/models.tar.gz .
   ## Then you need to adjust the location of the file you want to untar below in the tar command
   
   #untar just the hrrr model data we need for WPS (pressure fields)
   echo 'untar'
   tar -zxvf /uufs/chpc.utah.edu/common/home/horel-group/archive/$year$month$day/models.tar.gz --wildcards --no-anchored 'hrrr.t*z.wrfprsf00.grib2'  
   
   # Now go into that directory rename all the files with the date header
   echo 'rename files'
   cd $year$month$day/models/hrrr
   rename hrrr {$year}{$month}{$day}_hrrr hrrr*
   
   # Move those files to the directory the script is running. 
   # Keeping all the HRRR days in the same directory makes it easier for linking the grib files for ungribbing in WPS
   echo 'move files'
   mv *hrrr* ../../../
   # go back to directory we are running the script and remove the directory
   # For some reason, these empty directories wont be removed??
   cd ../../../
   pwd
   rmdir -p {$year}{$month}{$day}/models/hrrr
   
   # list the files so we can check they transfered over. Good idea to check if all hours are there.
   ls
end

echo ''
echo 'completed'
