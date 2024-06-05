'''
Description: Compute high-pass and low-pass of SLA satellite data using Fourier filter.
Author: Ligang Chen
Date created: 01/04/2024
Date last modified: 01/04/2024 
'''


import os
import datetime
import glob
import struct

import numpy as np
import xarray as xr
import pandas as pd

import sys
sys.path.append('/glade/u/home/lgchen/lib/fortran/f2py')
# import fort  # using F2PY call Fortran subroutine


def calc_low_pass_sla(pass_time, pass_sla):
    f = pass_sla
    N = len(f)
  # print('N = ', N)

    fl = np.zeros(N, dtype=np.float32)

    if N == 1:
        fl[0] = f[0]
        return fl

    a0 = np.mean(f)
    a = np.zeros(6, dtype=np.float32)  # only use 1~5, 
    b = np.zeros(6, dtype=np.float32)

    # calculate time intervals as weights
    total_t = pass_time[N-1] - pass_time[0]
    delta_t = []
    delta_t.append(pass_time[1] - pass_time[0])
    for i in range(1, N-1):
        delta_t.append((pass_time[i+1] - pass_time[i-1]) / 2)
    delta_t.append(pass_time[N-1] - pass_time[N-2])

    # calculate coefficients of cos and sin
    for i in range(1, 6): 
        for k in range(N): 
            w = 2.0 * delta_t[k] / total_t
            r = 2 * np.pi * i * (pass_time[k] - pass_time[0])/total_t
            a[i] = a[i] + w * f[k] * np.cos(r)
            b[i] = b[i] + w * f[k] * np.sin(r)

    a[5] = a[5]/2.
    b[5] = b[5]/2.

    # compute fl, and you can get fh = f - fl outside of this function
    for k in range(N):
        for i in range(1, 6):
            r = 2 * np.pi * i * (pass_time[k] - pass_time[0])/total_t
            fl[k] = fl[k] + a[i]*np.cos(r) + b[i]*np.sin(r)
        fl[k] = fl[k] + a0
    
    return fl




# DIR_DATA = '/glade/scratch/lgchen/data/OISSH_NOAA/2000-2022_fromEric'  # no longer exist
DIR_DATA = '/glade/u/home/lgchen/umcp0014/lgchen/OISSH_JEDI_DATA/2000-2022_fromEric'

missions = ['j1', 'j2', 'j3']
# jday_20020115 = datetime.date(2002,  1, 15)
jday_20150701 = datetime.date(2015,  7,  1)
jday_20150702 = datetime.date(2015,  7,  2)
# jday_20221231 = datetime.date(2022, 12, 31)

jday = jday_20150701
while jday <= jday_20150701:  # jday_20221231
    str_date = jday.strftime('%Y%m%d')
    print('current date: ', str_date)

    jday_prev = jday - datetime.timedelta(days=1)
    str_date_prev = jday_prev.strftime('%Y%m%d')

    jday_next = jday + datetime.timedelta(days=1)
    str_date_next = jday_next.strftime('%Y%m%d')

    for mi in missions:
        fn = mi + '_' + str_date + '.nc'
        if not os.path.exists(DIR_DATA + '/link/' + fn):
            continue

      # print('current mission: ', mi)
        ds = xr.open_dataset(filename_or_obj = DIR_DATA + '/link/' + fn, mask_and_scale = True, decode_times = True)
        fl = np.zeros(ds.dims['time'], dtype=np.float32)

        unique_pass = pd.unique(ds['pass'].values)  # pandas.unique(), not sorted which is what we want.
      # unique_pass = np.unique(ds['pass'].values)  # numpy.unique(), sorted!
        if np.all(np.diff(unique_pass) >= 0):  # case sorted ascending. 
            arr_1stIdxOfEachPass = np.searchsorted(ds['pass'].values, unique_pass, side='left')
        else:  # case not strictly ascending
            arr_1stIdxOfEachPass = np.nonzero(np.r_[1, np.diff(ds['pass'].values)])[0]

      # print('len(unique_pass): ', len(unique_pass))
      # print('len(arr_1stIdxOfEachPass): ', len(arr_1stIdxOfEachPass))
      # print('unique_pass: ', unique_pass)
      # print('arr_1stIdxOfEachPass: ', arr_1stIdxOfEachPass)
    

        if len(unique_pass) != len(arr_1stIdxOfEachPass):
            print('ERROR: len(unique_pass) != len(arr_1stIdxOfEachPass), fn = ', fn)
            exit()

        arr_1stIdxOfEachPass = np.append(arr_1stIdxOfEachPass, len(ds['pass']))  # need the last index
        
        for ip in range(len(unique_pass)):
          # print('current pass: ', unique_pass[ip])

            pass_time = ds['time_mjd'].values[arr_1stIdxOfEachPass[ip]:arr_1stIdxOfEachPass[ip+1]]
            pass_sla  = ds['sla'].values[arr_1stIdxOfEachPass[ip]:arr_1stIdxOfEachPass[ip+1]]
           
            if ip == 0:
                fn_prev = mi + '_' + str_date_prev + '.nc'
                if os.path.exists(DIR_DATA + '/link/' + fn_prev):
                    ds_prev = xr.open_dataset(filename_or_obj = DIR_DATA + '/link/' + fn_prev, mask_and_scale = True, decode_times = True) 
                    unique_pass_prev = pd.unique(ds_prev['pass'].values)
                    if unique_pass_prev[-1] == unique_pass[0]:
                      # 1stIdx = np.searchsorted(ds_prev['pass'].values, unique_pass_prev[-1], side='left')  # not necessarily sorted or ascending!!
                        # here if ds_prev only has 1 pass, the following assignment should be ok. 
                        firstIdx = np.nonzero(np.r_[1, np.diff(ds_prev['pass'].values)])[0][-1]
                        pass_time = np.append(ds_prev['time_mjd'].values[firstIdx:], pass_time)
                        pass_sla  = np.append(ds_prev['sla'].values[firstIdx:], pass_sla)
            elif ip == len(unique_pass) - 1:  # assume at least 2 passes in the file, what if there's only 1 pass?
                fn_next = mi + '_' + str_date_next + '.nc'
                if os.path.exists(DIR_DATA + '/link/' + fn_next):
                    ds_next = xr.open_dataset(filename_or_obj = DIR_DATA + '/link/' + fn_next, mask_and_scale = True, decode_times = True) 
                    unique_pass_next = pd.unique(ds_next['pass'].values)
                  # print('unique_pass_next: ', unique_pass_next)
                    if unique_pass_next[0] == unique_pass[-1]:
                      # lastIdx = np.searchsorted(ds_next['pass'].values, unique_pass_next[0], side='right')  # should be ok?
                        arr_1stIdxOfEachPass_next = np.nonzero(np.r_[1, np.diff(ds_next['pass'].values)])[0]
                        if len(arr_1stIdxOfEachPass_next) >= 2:
                            lastIdx = np.nonzero(np.r_[1, np.diff(ds_next['pass'].values)])[0][1]
                        else:  # case of only 1 pass, e.g. j1_20040215.nc
                            lastIdx = len(ds_next['pass'])
                        pass_time = np.append(pass_time, ds_next['time_mjd'].values[:lastIdx])
                        pass_sla  = np.append(pass_sla, ds_next['sla'].values[:lastIdx])

            fl_pass = calc_low_pass_sla(pass_time, pass_sla)

            if ip == 0:
                fl[ : arr_1stIdxOfEachPass[ip+1]] = fl_pass[-arr_1stIdxOfEachPass[1]:]
            elif ip == len(unique_pass) - 1:
                fl[arr_1stIdxOfEachPass[ip] : ] = fl_pass[ : arr_1stIdxOfEachPass[ip+1] - arr_1stIdxOfEachPass[ip]]
            else:
                fl[arr_1stIdxOfEachPass[ip] :arr_1stIdxOfEachPass[ip+1]] = fl_pass[:]
   
        # final daily low-pass file
        f = ds['sla'].values  # deep or shallow copy? maybe wrong. 
        ds['sla'].values = fl
        fn_lowpass = mi + '_' + str_date + '_lp.nc'
        ds.to_netcdf(DIR_DATA + '/FourierFilter/filtered/' + fn_lowpass, format="NETCDF3_CLASSIC")

        ds['sla'].values = f - fl
        fn_highpass = mi + '_' + str_date + '_hp.nc'
        ds.to_netcdf(DIR_DATA + '/FourierFilter/filtered/' + fn_highpass, format="NETCDF3_CLASSIC")       

    jday += datetime.timedelta(days=1)


