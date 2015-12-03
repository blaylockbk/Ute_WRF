# Brian Blaylock
# 3 December 2015

import numpy as np

def read_tslist(tsfile):
    """
    Reads in a time series list (tslist) in the WRFV3/test/em_real directory
    and puts the data in arrays for station name, id, lat, and lon.
    More info on the WRF tslist can be found here:
    http://www2.mmm.ucar.edu/wrf/users/docs/user_guide_V3/users_guide_chap5.htm#timeseries
    
    Input:
        file: the location of your tslist file
    Output:
        NAME: name of the station.
        STNID: id of the station. Preferably use the same as listed in MesoWest
               for easy API queries. 
        LAT: latitude of the station
        LON: longitude of the station
    """
    # Initialize the arrays
    NAME = np.array([])
    STNID= np.array([])
    LAT  = np.array([])
    LON  = np.array([])
    
    # Read each line of the text file
    with open(tsfile,'r') as f:
        for line in f:
            if line[0]=='#':
            # Discard the commented lines, first three lines of the tslist file
                continue
            # Grab the data from each line (throw away white spaces)
            NAME = np.append(NAME, line[0:25].strip())
            STNID = np.append(STNID, line[25:32].strip())
            LAT = np.append(LAT, float(line[32:41]))
            LON = np.append(LON, float(line[41:]))
    
    return NAME,STNID,LAT,LON


#--- Example -----------------------------------------------------------------#
if __name__ == "__main__":
    
    # Read the tslist file
    name,stn_id,lat,lon = read_tslist('./WRFV3/test/em_real/tslist')
    
    # Plot the locations of the sites
    import matplotlib.pyplot as plt
    plt.scatter(lon,lat)
    #Add Labels to each point
    for i in np.arange(0,len(stn_id)):
        plt.annotate(stn_id[i],xy=(lon[i],lat[i]))
      
    print "Station Names:"
    for i in name:
        print '  ',i
