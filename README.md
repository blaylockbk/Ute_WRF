THIS CODE IS SO OLD...best to scavage for parts.
![](https://github.com/blaylockbk/Ute_WRF/blob/master/rusty.jpg)

Ute-WRF/
==============

Mostly for post processing WRF output data.
Python codes that I've created at the University of Utah Mountain Meteorology Group.
For more info about running WRF see <http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/wrf.html>

    cross_section_*.py...............plot a cross section through the model domain (wrfout or auxhist files)
    
    plot_*.py........................plot a 2D map view of data at the surface or a model level
    
    tslist_*.py......................plot data from a ts file or vertical profile output
    
    


####Functions

"functions" folder includes functions dealing with various needs for processing WRF data. Note: some of these have been renamed since I wrote my other plotting scripts.

    custom_domains.py................dictionary of predefined subdomain lat/lon for plotting basemap
    
    landuse_colormap.py..............colormap for WRF landuse categories: MODIS20, MODIS21, NLCD, USGS
    
    terrain_colormap.py..............colormap for terrain. Set lake mask to low number for blue water
    
    read_tslist.py...................read data in the tslist file which includes station name, lat, lon
    
    get_ts_data.py...................loads station header, time series file, vertical profile variables
    
    trim_map.py......................trims wrf data. Useful if you have a large domain and only want a section
    
    wind_calcs.py....................convert from UV components to speed and direction, vice versa, etc.
    
    staggered_to_mass.py.............converts U and V variables on a staggered grid to the mass point value.

####Modificaitons

"modifications" folder includes modificaitons to WRF code.

  Initialize WRF with HRRR analyses (custom WPS tables):
  
    METGRID.TBL.HRRR.bkb...........................Metgrid Table for HRRR analyses
    
    Vtable.HRRR.bkb................................Vtable for HRRR analyses grib2 files
    
    
  Initialize and set continuous passive tracer:
  
    Registry.EM.bkb.tracer.........................Set new tracer variable in registry
    
    module_initialize_real.F.bkb.tracer............Initialize a passive tracer (code snippit)
    
    solve_em.bkb.tracer............................Create continuous tracer emit every timestep (code snippit)
    
  Modify Great Salt Lake tempertaure:
  
    module_initialize_real.F.bkb.LakeTemp..........Change Great Salt Lake temperature (code snippit)
    
  Modify Great Salt Lake Area in MODIS landuse category (do this in WPS geo.em files):
  
    shrink_GSL.py..................................Python script for changing lake area
    
####Other

"other" folder includes miscellaneous WRF code.
    
    tslist.bkb...............................tslist file for defining locations for WRF output at model time step
    
    untar_hrrr_files.csh.....................untar HRRR analyses from Horel Group archive
