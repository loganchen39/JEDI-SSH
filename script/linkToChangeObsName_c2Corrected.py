#!/usr/bin/env python3


import sys
import os
import datetime


sats = ['c2']
jday_st = datetime.date(2022, 2, 1)
jday_end = datetime.date(2022, 2, 28)
dir_obs_input = '/glade/scratch/lgchen/data/OISSH_NOAA/biasCorrection_crossoverAdjustment/correctedCrossovers_byLigang/c2_corrected_by_j3_for_all_nc3_format_ok'
dir_link_output = '/glade/scratch/lgchen/data/OISSH_NOAA/biasCorrection_crossoverAdjustment/correctedCrossovers_byLigang/link'

for sat in sats:
    jday = jday_st
    while jday <= jday_end:
      # fdate = datetime.datetime.combine(jday, datetime.time(12))
      # fn_in = sat + '_corrected_by_j3_' + jday.strftime('%Y%m%d') + '_no_w_all_s_0.nc'
      # fn_in = sat + '_corrected_by_j3_' + jday.strftime('%Y%m%d') + '_no_w_all_s_01.nc'
      # fn_in = sat + '_corrected_by_j3_' + jday.strftime('%Y%m%d') + '_no_w_all_s_02.nc'
      # fn_in = sat + '_corrected_by_j3_' + jday.strftime('%Y%m%d') + '_w_d_all_s_001.nc'
      # fn_in = sat + '_corrected_by_j3_' + jday.strftime('%Y%m%d') + '_w_d_all_s_005.nc'
      # fn_in = sat + '_corrected_by_j3_' + jday.strftime('%Y%m%d') + '_w_t_all_s_005.nc'
        fn_in = sat + '_corrected_by_j3_' + jday.strftime('%Y%m%d') + '_w_t_all_s_01.nc'
        fn_out = sat + '_' + jday.strftime('%Y%m%d') + '.nc'

        if os.path.isfile(dir_obs_input + '/' + fn_in):
          # str_cmd = 'ln -sf ' + dir_IODA_input + '/' + fn_in + ' ' + dir_link_output + '/' + fn_out
            os.symlink(dir_obs_input + '/' + fn_in, dir_link_output + '/w_t_all_s_01/' + fn_out)

        jday += datetime.timedelta(days=1)

