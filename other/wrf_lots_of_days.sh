#!/bin/bash

# Brian Blaylock
# August 4, 2015

# This will loop through each day and hour and create a WRF output file

year='2015'
month='05'
e_month='05'

# Loop over each day		
for d in 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31
do
	# Loop over each hour
		#for h in $(seq 00 23)
		#for h in 00
		for h in 23
		do
		  echo "Creating WRF Namelist for $year $month $d $h"
			next_hour=$(($h+1))
			next_hour=00
	         	next_day=$(($d+1))
		#	next_day=01
			echo "&time_control
 run_days                            = 0,
 run_hours                           = 1,
 run_minutes                         = 0,
 run_seconds                         = 0,
 start_year                          = $year,
 start_month                         = $month,
 start_day                           = $d,
 start_hour                          = $h,
 start_minute                        = 00,
 start_second                        = 00,
 end_year                            = $year,
 end_month                           = $e_month,
 end_day                             = $next_day,
 end_hour                            = $next_hour,
 end_minute                          = 00,
 end_second                          = 00,
 interval_seconds                    = 3600
 input_from_file                     = .true.,
 history_interval                    = 60,
 frames_per_outfile                  = 1000,
 restart                             = .false.,
 restart_interval                    = 720,
 io_form_history                     = 2
 io_form_restart                     = 2
 io_form_input                       = 2
 io_form_boundary                    = 2
 debug_level                         = 0
 /

 &domains
 time_step                           = 120,
 time_step_fract_num                 = 0,
 time_step_fract_den                 = 1,
 max_dom                             = 1,
 e_we                                = 350,
 e_sn                                = 350,
 e_vert                              = 51,
 p_top_requested                     = 5000,
 num_metgrid_levels                  = 41,
 num_metgrid_soil_levels             = 9,
 dx                                  = 3000,
 dy                                  = 3000,
 grid_id                             = 1,
 parent_id                           = 0,
 i_parent_start                      = 1,
 j_parent_start                      = 1,
 parent_grid_ratio                   = 1,
 parent_time_step_ratio              = 1,
 feedback                            = 1,
 smooth_option                       = 0
 eta_levels   =   1.0000, 0.9980, 0.9940, 0.9870, 0.9750, 0.9590,
          0.9390, 0.9160, 0.8920, 0.8650, 0.8350, 0.8020, 0.7660,
          0.7270, 0.6850, 0.6400, 0.5920, 0.5420, 0.4970, 0.4565,
          0.4205, 0.3877, 0.3582, 0.3317, 0.3078, 0.2863, 0.2670,
          0.2496, 0.2329, 0.2188, 0.2047, 0.1906, 0.1765, 0.1624,
          0.1483, 0.1342, 0.1201, 0.1060, 0.0919, 0.0778, 0.0657,
          0.0568, 0.0486, 0.0409, 0.0337, 0.0271, 0.0209, 0.0151,
          0.0097, 0.0047, 0.0000,
 /

 &physics
 mp_physics                          = 3,
 ra_lw_physics                       = 1,
 ra_sw_physics                       = 1, 
 radt                                = 30, 
 sf_sfclay_physics                   = 1, 
 sf_surface_physics                  = 1,
 bl_pbl_physics                      = 1,  
 bldt                                = 0,  
 cu_physics                          = 0, 
 cudt                                = 5,  
 isfflx                              = 1,
 ifsnow                              = 1,
 icloud                              = 1,
 surface_input_source                = 1,
 num_soil_layers                     = 4,
 sf_urban_physics                    = 0,  
 /

 &fdda
 /

 &dynamics
 w_damping                           = 0,
 diff_opt                            = 1,
 km_opt                              = 4,
 diff_6th_opt                        = 0,
 diff_6th_factor                     = 0.12,
 base_temp                           = 290.
 damp_opt                            = 1,
 zdamp                               = 5000.,
 dampcoef                            = 0.01,
 khdif                               = 0, 
 kvdif                               = 0,  
 non_hydrostatic                     = .true.,
 moist_adv_opt                       = 1,       
 scalar_adv_opt                      = 1,     
 do_avgflx_em                        = 1, 1, 1, 1, 1, 1, 1, 1, 1,
 do_avgflx_cugd                      = 1, 1, 1, 1, 1, 1, 1, 1, 1,
 /

 &bdy_control
 spec_bdy_width                      = 5,
 spec_zone                           = 1,
 relax_zone                          = 4,
 specified                           = .true.,
 nested                              = .false.,
 /

 &grib2
 /

 &namelist_quilt
 nio_tasks_per_group = 0,
 nio_groups = 1,
 /" > namelist.input


echo "

run real.exe
"
mpirun -np 12 ./real.exe 

tail rsl.out.0000
echo "

run wrf.exe
"
mpirun -np 12 ./wrf.exe
	
tail rsl.out.0000			

mv wrfout_d01_2015-$month-$d* ~/../horel-group4/songnex/HRRR_wrf/


			done

done


