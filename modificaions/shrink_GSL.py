# Brian Blaylock
# November 19, 2015

# Script for decreasing the size of the Great Salt Lake (GSL) to
# a more realistic lake level. Uses the python basemap outline of the GSL, which 
# is more current than MODIS, to shrink the lake.
# The basemap function "maskocean" is used to mask out the lake area.

# I make the modification in the geo_em.d0*.nc files for each domain after running GEOGRID

#from netCDF4 import Dataset  # we dont have this library. Use scipy instead
from scipy.io import netcdf
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, maskoceans
import numpy as np
import os
import shutil

from fucntions.custom_domains import get_domain # you don't have to have this
                                                # It's just a dictionary of lats/lons for
                                                # predefined lat/lon boundaries around the lake.

def cut_data(bl_lat,tr_lat,bl_lon,tr_lon,lat,lon,buff=0):
    '''    
    Cut down data for domain for faster plotting.
        
    input: the bottom left corner and top right corner lat/lon coordinates
        bl_lat = bottom left latitude
        tr_lat = top right latitude
        bl_lon = bottom left longitude
        tr_lon = top right longitude
        buff   = is a buffer in case the domain is skewed resulting in blank spots
                 on the map plot.
    return: the max and min of each the arrays x and y coordinates    
    
    '''
    lat_limit = np.logical_and(lat>bl_lat,lat<tr_lat)
    lon_limit = np.logical_and(lon>bl_lon,lon<tr_lon)
    
    total_limit = np.logical_and(lat_limit,lon_limit)
    
    xmin = np.min(np.where(total_limit==True)[0])-buff # +/- a buffer to cover map area 
    xmax = np.max(np.where(total_limit==True)[0])+buff
    ymin = np.min(np.where(total_limit==True)[1])-buff
    ymax = np.max(np.where(total_limit==True)[1])+buff
    
    return xmin,xmax,ymin,ymax                                                
                                                
def fix_nonlake_val(original, lat, lon, new_value):
    """
    Function creates a new array of the original variable with lake modification.
    
    Input the original 2D array, specify the new value.
    Everything that isn't a python basemap defined GSL will be replaced with 
    the new value.
        Example 1)
        For original=lakemask
        If it's not really lake, then replace with 1 (land).
        Example 2)
        For original=lake_depth
        If it's not really lake, then replace with a depth (10).
        
    """
    
    # 1) We don't want to replace all the water points in the state, just 
    #    arount the GSL. So, grab a subdomain...

    # cut the data points to our GSL cut domain from my custom domain dictionary
    GSL = get_domain('great_salt_lake_cut')
    bl_lat = GSL['bot_left_lat']
    bl_lon = GSL['bot_left_lon']
    tr_lat = GSL['top_right_lat']
    tr_lon = GSL['top_right_lon']
    ymin,ymax,xmin,xmax = cut_data(bl_lat,tr_lat,bl_lon,tr_lon,lat,lon) 
    #These are the index value max/mins for the section of interest

    
    
    # 2) Use maskoceans to identify points that are not lake based on pythons 
    #    basemap. (see main part of code for this variable)   

    #   shrink_lake is a masked array.
    #   shrink_lake.mask is a true/false array that tells us if the data point
    #   are (True) or are not (False) lake.
    
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
    # Add water back in Willard Bay
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
    Function plots the change so you can visually compare the 
    modification and asks if you wish to save the new value.
    If it looks good, saves the new data.
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
    
    ## Draw Box Elder County water area shapefile to locate Willard Bay
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

#domain = 'd01'
domain = 'd02'
BASE = '/uufs/chpc.utah.edu/common/home/horel-group4/model/bblaylock/WRF3.7_kingspeakTest/WPS/'
FILE = 'geo_em.%s.nc' % domain
HOME = '/uufs/chpc.utah.edu/common/home/u0553130/'
nc = netcdf.netcdf_file(BASE+FILE,'r')

# Make a copy of the original that we will write the new data to.
NEW_FILE = BASE+'lakesnip_'+FILE # new file name
shutil.copy2(BASE+FILE,NEW_FILE) # copy the original file

#====================================================
# Get variables from NetCDF file
#====================================================
# Open the XLAT, XLON variable
lat = nc.variables['XLAT_M'][0]
lat = lat.copy()
lon = nc.variables['XLONG_M'][0]
lon = lon.copy()

# Open the variables that need to be changed to fix lake area
landmask = nc.variables['LANDMASK'][0].copy()
lakedepth = nc.variables['LAKE_DEPTH'][0].copy()
LandUseCat = nc.variables['LU_INDEX'][0].copy()
#additional variables needed to change (03/28/2016)
SoilBot = nc.variables['SCB_DOM'][0].copy()
SoilTop = nc.variables['SCT_DOM'][0].copy()



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
                     inlands=True,   # we want to include lakes in our mask (not all the world's lakes are included in the python basemap)
                     resolution='f', # get the highest resolution
                     grid=1.25)      # and the best grid spacing in basemap

#====================================================
# Fix values that aren't really lake
#====================================================
new_landmask = fix_nonlake_val(landmask,lat,lon,1)      # If it's not lake, then make it land (1)
new_lakedepth = fix_nonlake_val(lakedepth,lat,lon,10)   # If it's not lake, then set to the standard depth (10)
new_LandUseCat = fix_nonlake_val(LandUseCat,lat,lon,16) # If it's not lake, then set as "barren or Sparely vegetated" (16)

# additional mods (thanks Matthew Scutter) (03/28/2016)
new_SoilBot = fix_nonlake_val(SoilBot,lat,lon,8) # If it's not lake, then set as "silty clay loam" (8)
new_SoilTop = fix_nonlake_val(LandUseCat,lat,lon,11) # If it's not lake, then set as "Silty Clay" (11)

#====================================================
# Confirm and save changes
#====================================================
confirm_save(landmask,new_landmask,'LANDMASK',lat,lon,NEW_FILE)
confirm_save(lakedepth,new_lakedepth,'LAKE_DEPTH',lat,lon,NEW_FILE)
confirm_save(LandUseCat,new_LandUseCat,'LU_INDEX',lat,lon,NEW_FILE)

# additional mods (thanks Matthew Scutter) (03/28/2016)
confirm_save(SoilBot,new_SoilBot,'SCB_DOM',lat,lon,NEW_FILE)
confirm_save(SoilTop,new_SoilTop,'SCT_DOM',lat,lon,NEW_FILE)
