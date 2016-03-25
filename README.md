Ute-WRF/
==============

Mostly python codes that I've created at the University of Utah Mountain Meteorology Group.
These are scripts for processing WRF NetCDF files.



---------------------------------------------------------------------------------------------
         TSLIST
---------------------------------------------------------------------------------------------
"tslist" folder includes scripts for dealing with the high resolution output for stations
defined in the tslist


---------------------------------------------------------------------------------------------
         MODIFICATIONS
---------------------------------------------------------------------------------------------
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
    
  


