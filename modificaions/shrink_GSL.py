# Brian Blaylock
# November 19, 2015

# Script for decreasing the size of the Great Salt Lake to
# a more realistic lake level.

#from netCDF4 import Dataset  # we dont have this library. use scipy instead
from scipy.io import netcdf
#matplotlib.use('Agg')		#required for the CRON job. Says, "do not open plot in a window"??
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, maskoceans
import numpy as np
import os
import shutil

from functions_domains_models import *



def fix_nonlake_val(original, lat, lon, new_value):
    """
    Input the original 2D array, specify the new value.
    Everything that isn't a python basemap defined GSL will be replaced with 
    the new value.
        Example 1)
        original=lakemask. If it's not really lake, then replace with 1 (land).
        Example 2)
        original=lake_depth. If it's not really lake, then replace with a depth (10).
        
        two_way set to true will convert all non-lake points to its origianl.
    """
    
    # 1) We don't want to replace all the water points in the state, just 
    #    arount the GSL. So, grab a subdomain...

    # cut the data points to our GSL cut domain
    GSL = get_domain('great_salt_lake_cut')
    bl_lat = GSL['bot_left_lat']
    bl_lon = GSL['bot_left_lon']
    tr_lat = GSL['top_right_lat']
    tr_lon = GSL['top_right_lon']
    ymin,ymax,xmin,xmax = cut_data(bl_lat,tr_lat,bl_lon,tr_lon,lat,lon) 
    #There, these are the index value max/mins for the section of interest

    
    # 2) Use maskoceans to identify points that are not lake based on pythons 
    #    basemap.   
    

    # shrink_lake is a masked array.
    # shrink_lake.mask is a true/false array that tells us if the data point
    # are (True) or are not (False) lake.
    
    # 3) Make a copy of the original data. We will replace the non-lake points 
    #    with a new value. We make an intermediate (i) lake where we change
    #    all the masked points in the entire domain (we will use these changes
    #    to create the final form in step 4)
    i_lake = original.copy()
    
    #If point is not really ocean/lake (if it is land) then set with new value
    # False == Land
    remove_lake = np.logical_and(landmask==0,shrink_lake.mask==False)    
    i_lake[remove_lake]=new_value
    #i_lake[shrink_lake.mask==False] = new_value
    
    ## !IMPORTANT! We don't replace WRF land points with python lake points. 
    ## In other words, if WRF says it's land, keep it land. 
    ## Else, uncomment the line below and make adjustment to new_value...
    #i_lake[shrink_lake.mask==True] = 0 # if point is ocean/lake, set landmask to ocean 
    
    # 4) Ok, now we have changed all the points in the entire domain based on
    #    the shrink_lake mask. Now we only want to make changes to the
    #    subdomain, the region right around the lake as we defined in step 1.
    new_lake = original.copy()
    new_lake[ymin:ymax,xmin:xmax] = i_lake[ymin:ymax,xmin:xmax]
    
    # 5) Make any other changes few changes in any extra spots
    # Add water in Willard Bay
    sub = get_domain('willard_bay')
    bl_lat = sub['bot_left_lat']
    bl_lon = sub['bot_left_lon']
    tr_lat = sub['top_right_lat']
    tr_lon = sub['top_right_lon']
    ymin,ymax,xmin,xmax = cut_data(bl_lat,tr_lat,bl_lon,tr_lon,lat,lon)     
    new_lake[ymin:ymax,xmin:xmax] = original[ymin:ymax,xmin:xmax]
    
    # 5) Finally, return the new_lake 2D array.
    return new_lake
    

def confirm_save(old,new,replace_this, lat, lon, NEW_FILE):
    """
    Plots the change and asks if you wish to save the new value
    """
     
    x,y = m(lon,lat)
    
    plt.suptitle("Check to make sure these changes look right for "+replace_this)
    
    plt.subplot(1,3,1)
    m.drawstates(color='k', linewidth=.8)
    m.drawcoastlines(color='k')
    m.drawcountries(color='k', linewidth=1.25)
    plt.pcolormesh(x,y,old)
    plt.title('Before Surgery')
    
    plt.subplot(1,3,2)
    plt.title('After Surgery')
    
    # Draw the area that we have modified
    GSL = get_domain('great_salt_lake_cut')
    toprightlat = GSL['top_right_lat']
    topleftlat = GSL['top_right_lat']
    toprightlon = GSL['top_right_lon']
    topleftlon = GSL['bot_left_lon']
    botrightlat = GSL['bot_left_lat']
    botrightlon = GSL['top_right_lon']
    botleftlat = GSL['bot_left_lat']
    botleftlon = GSL['bot_left_lon']
    
    m.drawgreatcircle(toprightlon,toprightlat,topleftlon,topleftlat, color='#FFFF4C', linewidth='3')
    m.drawgreatcircle(topleftlon,topleftlat,botleftlon,botleftlat, color='#FFFF4c', linewidth='3')
    m.drawgreatcircle(botleftlon,botleftlat,botrightlon,botrightlat, color='#FFFF4c', linewidth='3')
    m.drawgreatcircle(botrightlon,botrightlat,toprightlon,toprightlat, color='#FFFF4c', linewidth='3')
    
    ## Draw Box Elder County water area to locate Willard Bay
    #m.readshapefile(HOME+'shape_files/tl_2015_BoxElder_areawater/tl_2015_49003_areawater','roads', linewidth=.25)
    
    m.drawstates(color='k', linewidth=.8)
    m.drawcoastlines(color='k')
    m.drawcountries(color='k', linewidth=1.25)
    plt.pcolormesh(x,y,new)
    
    plt.subplot(1,3,3)
    plt.title('Difference')
    m.drawstates(color='k', linewidth=.8)
    m.drawcoastlines(color='k')
    m.drawcountries(color='k', linewidth=1.25)
    plt.pcolormesh(x,y,old-new,cmap="bwr")   
    
    
    plt.show()
    
    print "Going to replace ",replace_this," variable."
    good_to_go = raw_input("Does this look good? (y/n): ")
    if good_to_go=='y':
        print "Ok, saving a new geo file for WRF: "+BASE+'lakesnip_'+FILE    
    
        #Open Copied File in append mode
        nc_copy = netcdf.netcdf_file(NEW_FILE,'a')
        nc_copy.variables[replace_this][0] = new
        nc_copy.sync()
        nc_copy.close()
        
        print "Edited the new NetCDF file. View and check with ncview"    


#==============================================================================
#==============================================================================

#====================================================
# Open the geo_em files for each domain
#====================================================

domain = 'd01'
BASE = '/uufs/chpc.utah.edu/common/home/horel-group4/model/bblaylock/WRF3.7_kingspeakTest/WPS/'
FILE = 'geo_em.%s.nc' % domain
HOME = '/uufs/chpc.utah.edu/common/home/u0553130/'
nc = netcdf.netcdf_file(BASE+FILE,'r')

# Make a copy of the original that we will write the new data to.
NEW_FILE = BASE+'lakesnip_'+FILE

shutil.copy2(BASE+FILE,NEW_FILE)

#====================================================
# Get variables from NetCDF file
#====================================================
# Open the XLAT, XLON variable
lat = nc.variables['XLAT_M'][0]
lat = lat.copy()
lon = nc.variables['XLONG_M'][0]
lon = lon.copy()
# Open the variable that needs to be changed to fix lake area
landmask = nc.variables['LANDMASK'][0].copy()
lakedepth = nc.variables['LAKE_DEPTH'][0].copy()
LandUseCat = nc.variables['LU_INDEX'][0].copy()


#====================================================
# Set up basemap
#====================================================
# Domain Boundaries
bot_left_lat  = lat[0][0]-.5 
bot_left_lon  = lon[0][0]-.5
top_right_lat = lat[-1][-1]+.5
top_right_lon = lon[-1][-1]+.5

# Create Basemap
MP = 'cyl'
if MP == 'cyl':
    ## Map in cylindrical projection (data points may apear skewed)
    m = Basemap(resolution='i',area_thresh=1.,projection='cyl',\
        llcrnrlon=bot_left_lon,llcrnrlat=bot_left_lat,\
        urcrnrlon=top_right_lon,urcrnrlat=top_right_lat,)

if MP == 'lcc':
    ## Map in HRRR projected Coordinates
    m = Basemap(resolution='i',area_thresh=1.,projection='lcc',\
        lat_0=38.5,lon_0=-97.5,\
        lat_1=38.5, lat_2=38.5,\
        llcrnrlon=bot_left_lon,llcrnrlat=bot_left_lat,\
        urcrnrlon=top_right_lon,urcrnrlat=top_right_lat,)

# This is step 2 of the function fix_nonlake_val
# We do this outside the function so we only have to calculate it once.
shrink_lake = maskoceans(lon,lat,landmask,
                     inlands=True,   # we want to include lakes in our mask
                     resolution='f', # get the highest resolutoin
                     grid=1.25)      # and the best grid spacing in basemap

#====================================================
# Fix values that aren't really lake
#====================================================
new_landmask = fix_nonlake_val(landmask,lat,lon,1) # If it's not lake, then make it land (1)
new_lakedepth = fix_nonlake_val(lakedepth,lat,lon,10) # If it's not lake, then make the standard depth (10)
new_LandUseCat = fix_nonlake_val(LandUseCat,lat,lon,16) # If it's not lake, then set at Barren or Sparcly vegetated (16)

#====================================================
# Confirm and save changes
#====================================================
confirm_save(landmask,new_landmask,'LANDMASK',lat,lon,NEW_FILE)
confirm_save(lakedepth,new_lakedepth,'LAKE_DEPTH',lat,lon,NEW_FILE)
confirm_save(LandUseCat,new_LandUseCat,'LU_INDEX',lat,lon,NEW_FILE)
