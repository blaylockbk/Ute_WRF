## Custom Landuse ColorMaps by Brian

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

# Four Different Land Use Categories you can use in WRF:
#   LU_MODIS20
#   LU_MODIS21     includes lake category
#   LU_USGS
#   LU_NLCD


## Land Use Colormap
## ! represents categories not in my Utah domain
def LU_MODIS21(): #
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
    [0,0,.88],        #  17 Water
    [.86,.08,.23],        #  18 Wooded Tundra
    [.97,.5,.31],        #! 19 Mixed Tundra
    [.91,.59,.48],     #! 20 Barren Tundra
    [.5,.7,1]])    #! 21 Lake

    cm = ListedColormap(C)
    
    labels = ['Evergreen Needleleaf Forest',
              'Evergreen Broadleaf Forest',
              'Deciduous Needleleaf Forest',
              'Deciduous Broadleaf Forest',
              'Mixed Forests',
              'Closed Shrublands',
              'Open Shrublands',
              'Woody Savannas',
              'Savannas',
              'Grasslands',
              'Permanent Wetlands',
              'Croplands',
              'Urban and Built-Up',
              'Cropland/Natural Vegetation Mosaic',
              'Snow and Ice',
              'Barren or Sparsely Vegetated',
              'Water',
              'Wooded Tundra',
              'Mixed Tundra',
              'Barren Tundra',
              'Lake']    
    
    return cm, labels

def LU_MODIS20(): #
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
    [0,0,.88],        #  17 Water
    [.86,.08,.23],        #  18 Wooded Tundra
    [.97,.5,.31],        #! 19 Mixed Tundra
    [.91,.59,.48]])     #! 20 Barren Tundra

    cm = ListedColormap(C)
    
    labels = ['Evergreen Needleleaf Forest',
              'Evergreen Broadleaf Forest',
              'Deciduous Needleleaf Forest',
              'Deciduous Broadleaf Forest',
              'Mixed Forests',
              'Closed Shrublands',
              'Open Shrublands',
              'Woody Savannas',
              'Savannas',
              'Grasslands',
              'Permanent Wetlands',
              'Croplands',
              'Urban and Built-Up',
              'Cropland/Natural Vegetation Mosaic',
              'Snow and Ice',
              'Barren or Sparsely Vegetated',
              'Water',
              'Wooded Tundra',
              'Mixed Tundra',
              'Barren Tundra']
    
    return cm, labels
    
    
def LU_USGS():
    # Provided by Chris Foster
    C = np.array([
    [0.0, 0.0, 1.0],
    [0.0, 1.0, 1.0],
    [0.4, 0.4, 0.4],
    [0.0, 0.4, 0.2],
    [0.2, 0.6, 0.2],
    [0.3, 0.7, 0.0],
    [0.8, 1.0, 0.2],
    [0.0, 1.0, 0.0],
    [0.8, 0.4, 0.2],
    [0.6, 0.4, 0.0],  
    [1.0, 1.0, 1.0]   
    ])
    
    cm = ListedColormap(C)
    
    labels = ['Water',   
    'Wetland',
    'Devloped Urban',     
    'Evergreen Forest', 
    'Deciduous Forest',    
    'Irrigated Cropland and Pasture', 
    'Cropland/Grassland Mosaic', 
    'Grassland', 
    'Shrubland', 
    'Barren Land', 
    'High Albedo Surface'
    ]
    
    return cm, labels
    
def LU_NLCD():
    # Provided by Chris Foster
    C = np.array([
    [0.0, 0.0, 1.0],
    [0.0, 1.0, 1.0],
    [0.3, 0.3, 0.3],
    [0.4, 0.4, 0.4],
    [0.5, 0.5, 0.5],
    [0.6, 0.6, 0.6],
    [0.0, 0.4, 0.2],
    [0.2, 0.6, 0.2],
    [0.3, 0.7, 0.0],
    [0.8, 1.0, 0.2],
    [0.0, 1.0, 0.0],
    [0.8, 0.4, 0.2],
    [0.6, 0.4, 0.0]
    ])
    
    cm = ListedColormap(C)
    
    labels = ['Water',
    'Wetland',
    'Developed High Intensity', 
    'Developed Medium Intensity',  
    'Developed Low Intensity', 
    'Developed Open Space', 
    'Evergreen Forest', 
    'Deciduous Forest', 
    'Cultivated Crops', 
    'Pasture/Hay', 
    'Grassland', 
    'Shrubland', 
    'Barren Land' 
    ]
    
    return cm, labels

if __name__ == "__main__":
    
    # Example Usage. Take note of the special parameters in pcolormesh and colorbar. There is no category '0' so start with 1
    
    # Grab colormap and labels
    cm,labels = LU_MODIS21()
    
    #create some Land Use category field
    LU_INDEX = np.random.randint(0,len(labels)+1,(20,20))
    
    plt.figure(1)
    plt.title('Land Use Categories')
    plt.pcolormesh(LU_INDEX,cmap = cm,vmin=1,vmax=len(labels)+1)
    cbar = plt.colorbar()
    cbar.set_ticks(np.arange(0.5,len(labels)+1)) # puts tick in middle of colored box rather than top
    cbar.ax.set_yticklabels(labels)
    #cbar.ax.set_yticklabels(np.arange(1,len(labels)+1))
    

    
