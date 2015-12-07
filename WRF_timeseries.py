# Brian Blaylock
# 4 December 2015

# Two functions to process data in a TS file outputted by WRF.
#   get_ts_header reads the header and puts the data in a dictionary.
#   get_ts_data reads the data and puts a variable in a numpy array.

# More information about WRF's tslist can be found in the WRF directory
# WRFV3/run/README.tslist

import linecache
import numpy as np

def get_ts_header(TSfile):
    """
    Returns a dictionary with information contined in the header of the TSfile
    produced by WRF.
    
    Input:
        TSfile - The time series output produced by WRF in the form XXX.d0Y.TS
                 where XXX is the station ID and Y is the domain.
    Output:
        header_dict - A dictionary that contains the following:
            stn_name    = string of the station's full name
            grid_id     = string of the station's ID
            stn_id      = tuple of the station's grid ID
            stn_latlon  = list of the station's real latitude and longitude
            grid_indices= tuple of the grid indices. Location on domain.
            grid_latlon = list of the grid latitude and longitude
            grid_elev   = float of the grid elevation
            elev_units       = units of the elevation 
    """
    line = linecache.getline(TSfile,1)
    
    name = line[0:25]
    gridID1 = line[26:29]
    gridID2 = line[29:32]
    stnID = line[33:38]
    stnlat = line[39:46]
    stnlon = line[47:55]
    gridindx1 = line[58:62]
    gridindx2 = line[63:67]
    gridlat = line[70:77]
    gridlon = line[78:86]
    grid_elev = line[88:94]
    elev_units = line[95:]
    
    header_dict = {
                    'stn_name':name.strip(),
                    'grid_id':(int(gridID1),int(gridID2)),
                    'stn_id':stnID.strip(), 
                    'stn_latlon':[float(stnlat),float(stnlon)],
                    'grid_indices':(int(gridindx1),int(gridindx2)),
                    'grid_latlon':[float(gridlat),float(gridlon)],
                    'grid_elev':float(grid_elev),
                    'elev_units':elev_units.strip()                      
                    }
    return header_dict

def get_ts_data(TSfile,variable):
    """
    Opens the tslist output. Packages and returns the data.
    The tslist oupt     
    
    Input:
        TSfile - The time series output produced by WRF in the form XXX.d0Y.TS
                 where XXX is the station ID and Y is the domain number
        variable - The variable in the TSfile you wish to retrieve
            id:          grid ID
            ts_hour:     forecast time in hours
            id_tsloc:    time series ID
            ix,iy:       grid location (nearest grid to the station)
            t:           2 m Temperature (K)
            q:           2 m vapor mixing ratio (kg/kg)
            u:           10 m U wind (earth-relative)
            v:           10 m V wind (earth-relative)
            psfc:        surface pressure (Pa)
            glw:         downward longwave radiation flux at the ground (W/m^2, downward is positive)
            gsw:         net shortwave radiation flux at the ground (W/m^2, downward is positive)
            hfx:         surface sensible heat flux (W/m^2, upward is positive)
            lh:          surface latent heat flux (W/m^2, upward is positive)
            tsk:         skin temperature (K)
            tslb(1):     top soil layer temperature (K)
            rainc:       rainfall from a cumulus scheme (mm)
            rainnc:      rainfall from an explicit scheme (mm)
            clw:         total column-integrated water vapor and cloud variables
            
    Output:
        A numpy array of the data for the variable you requrested
    """
    # column names as defined by the WRFV3/run/README.tslist
    col_names = ['id','ts_hour','id_tsloc','ix','iy','t','q','u','v','psfc',
                 'glw','gsw','hfx','lh','tsk','tsbl','rainc','rainnc','clw']
    
    # check that the input variable matches with one in the list
    if variable not in col_names:
        print "That variable is not available. Choose a variable from the following list"
        print "\
        'id'           grid ID\n\
        'ts_hour':     forecast time in hours\n\
        'id_tsloc':    time series ID\n\
        'ix':          grid location (nearest grid to the station)\n\
        'iy':          grid location (nearest grid to the station)\n\
        't':           2 m Temperature (K)\n\
        'q':           2 m vapor mixing ratio (kg/kg)\n\
        'u':           10 m U wind (earth-relative)\n\
        'v':           10 m V wind (earth-relative)\n\
        'psfc':        surface pressure (Pa)\n\
        'glw':         downward longwave radiation flux at the ground (W/m^2, downward is positive)\n\
        'gsw':         net shortwave radiation flux at the ground (W/m^2, downward is positive)\n\
        'hfx':         surface sensible heat flux (W/m^2, upward is positive)\n\
        'lh':          surface latent heat flux (W/m^2, upward is positive)\n\
        'tsk':         skin temperature (K)\n\
        'tslb':        top soil layer temperature (K)\n\
        'rainc':       rainfall from a cumulus scheme (mm)\n\
        'rainnc':      rainfall from an explicit scheme (mm)\n\
        'clw':         total column-integrated water vapor and cloud variables\n\n"

    
    # load the file into a numpy array
    TS = np.genfromtxt(TSfile, skip_header=1, names = col_names)
 
    return TS[variable]


#--- Example -----------------------------------------------------------------#
if __name__ == "__main__":
    
    wrf_dir = '/uufs/chpc.utah.edu/common/home/horel-group4/model/bblaylock/WRF3.7_sniplake/WRFV3/test/em_real/'    
    tsfile = 'KSLC.d02.TS'    

    # Use above function to get the header dictionary    
    header = get_ts_header(wrf_dir+tsfile)
    
    # Print all the keys and values in the header dictionary    
    print "\nHeader info from", tsfile    
    for i in header:
        print '  ',i, '=',header[i]
    print ""
    
    
    # Use above function to get the data for a few variables
    temp_2m = get_ts_data(wrf_dir+tsfile,'t')
    u_10m = get_ts_data(wrf_dir+tsfile,'u')
    
