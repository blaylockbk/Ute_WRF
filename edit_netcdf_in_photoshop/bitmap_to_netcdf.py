## Brian Blaylock
## 20 May 2016

### !Not finished. Just saving my progress!

# Convert image to array and to netCDF

# This method may only work for arrays with less than 255 unique values. That is all an image can distinguish
# This is useful for categorical data and masked data sets,
# but not for range data like temperature or elevation


import numpy as np
import os

#-------------------
## MODIS 21 category land use
C = np.array([
    [0,.4,0],      #  1 Evergreen Needleleaf Forest
    [0,.4,.2],      #! 2 Evergreen Broadleaf Forest    
    [.2,.8,.2],     #  3 Deciduous Needleleaf Forest
    [.2,.8,.4],     #  4 Deciduous Broadleaf Forest
    [.2,.6,.2],     #  5 Mixed Forests
    [.3,.7,0],      #  6 Closed Shrublands
    [.82,.41,.12],     #  7 Open Shurblands
    [.74,.71,.41],       #  8 Woody Savannas
    [1,.84,.0],     #  9 Savannas
    [0,1,0],        #  10 Grasslands
    [0,1,1],        #! 11 Permanant Wetlands
    [1,1,0],      #  12 Croplands
    [1,0,0],     #  13 Urban and Built-up
    [.7,.9,.3],      #! 14 Cropland/Natual Vegation Mosaic
    [1,1,1],        #! 15 Snow and Ice
    [.914,.914,.7], #  16 Barren or Sparsely Vegetated
    [.5,.7,1],        #  17 Water (like oceans)
    [.86,.08,.23],        #  18 Wooded Tundra
    [.97,.5,.31],        #! 19 Mixed Tundra
    [.91,.59,.48],     #! 20 Barren Tundra
    [0,0,.88]])      #! 21 Lake

#-------------------


from scipy import misc
path = './'
image= misc.imread(os.path.join(path,'landuse1.bmp'), flatten= 0)
image = np.round((image/255.),2)


lu = np.zeros(image.shape[0:2])

for i in np.arange(1,len(C)+1):  
    lu[image[:,:,0]==.5] =17

    # etc...


landuse = misc.imread(os.path.join(path,'landuse2.bmp'), flatten= 0)
elevation = misc.imread(os.path.join(path,'elevation2.bmp'), flatten= 0)
landmask = misc.imread(os.path.join(path,'landmask2.bmp'), flatten= 0)

## Show the difference between the original Land Use and modified
## open and save as NetCDF in place of old land_use


import matplotlib.pyplot as plt

plt.imshow(lu)
plt.show()

plt.contourf(lu,cmap='binary')            
plt.show()
