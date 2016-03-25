Ute-WRF/
==============

Mostly python codes that I've created at the University of Utah Mountain Meteorology Group.




####Functions

"functions" folder includes functions dealing with various needs for processing WRF data.

    custom_domains.py................dictionary of predefined subdomain lat/lon for plotting basemap
    
    landuse_colormap.py..............colormap for WRF landuse categories: MODIS20, MODIS21, NLCD, USGS
    
    terrain_colormap.py..............colormap for terrain. Set lake mask to low number for blue water
    
    read_tslist.py...................read data in the tslist file which includes station name, lat, lon
    
    get_ts_data.py...................loads station header, time series file, vertical profile variables
    
    trim_map.py......................trims wrf data. Useful if you have a large domain and only want a section
    
    wind_calcs.py....................convert from UV components to speed and direction, vice versa, etc.

####Modificaitons

"modifications" folder includes modificaitons to WRF code.

  Initialize WRF with HRRR analyses (custom WPS tables):
  
    METGRID.TBL.HRRR.bkb...................................Metgrid Table for HRRR analyses
    
    Vtable.HRRR.bkb........................................Vtable for HRRR analyses grib2 files
    
    
  Initialize and set continuous passive tracer:
  
    module_initialize_real.F.bkb.tracer....................Initialize a passive tracer (code snippit)
    
    solve_em.bkb.tracer....................................Create continuous tracer emit every timestep (code snippit)
    
  Modify Great Salt Lake tempertaure:
  
    module_initialize_real.F.bkb.LakeTemp..................Change Great Salt Lake temperature (code snippit)
    
  Modify Great Salt Lake Area in MODIS landuse category (do this in WPS geo.em files):
  
    shrink_GSL.py..........................................Python script for changing lake area
    
    
  


