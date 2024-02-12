'''
Description: Compute binned/average result on OI 0.25-degree grid from 1D High and Low pass of
             j1/j2/j3 satellite SSH. 
Author: Ligang Chen
Date created: 01/11/2024
Date last modified: 01/11/2024 
'''

import numpy as np
import xarray as xr
import pandas as pd

import os
import calendar
import datetime
import glob

import sys
sys.path.append('/glade/work/lgchen/lib/mylib_repo/f2py')

import fort  # using F2PY call Fortran subroutine

# np.set_printoptions(threshold=np.inf) # To print all numpy array elements.


DIR_DATA = '/glade/u/home/lgchen/lgchen_scratch_cheyenne/data/OISSH_NOAA/2000-2022_fromEric/FourierFilter'

ds_ana = xr.open_dataset(filename_or_obj=DIR_DATA+'/misc/ana.2022011512.withCoords.nc')
lat_oi = ds_ana.coords['lat']  # 720: -89.875, -89.625, -89.375, ...,  89.375,  89.625,  89.875, .values? 
lon_oi = ds_ana.coords['lon']  # 1440: -179.875, -179.625, ..., 179.875  # 0.125 0.375 0.625 ... 359.625 359.875
# print('lat_oi: ', lat_oi)
# print('lon_oi: ', lon_oi)
landmask_oi = xr.where(ds_ana['seaSurfaceHeightAnomaly'].isnull(), 0, 1).astype(np.int32)  # .astype(np.int32)? 
landmask_oi = landmask_oi[0, :, :].T
# print(landmask_oi)


missions = ['j1', 'j2', 'j3']
passes = ['hp', 'lp']

# daily, no daytime and nighttime.
daily_sla_avg = np.zeros((1440, 720), dtype=np.float32, order='F') 
daily_sla_num = np.zeros((1440, 720), dtype=np.int32  , order='F')


jday_20020115 = datetime.date(2002,  1, 15)
jday_20221231 = datetime.date(2022, 12, 31)

jday = jday_20020115
while jday <= jday_20221231:
    str_date = jday.strftime('%Y%m%d')
    print('current date: ', str_date)

    for mi in missions:
        for p in passes:
            fn = mi + '_' + str_date + '_' + p + '.nc'
            if not os.path.exists(DIR_DATA + '/filtered/' + fn):
                continue

            ds = xr.open_dataset(filename_or_obj = DIR_DATA + '/filtered/' + fn, mask_and_scale = True, decode_times = True)

            idx_lat = np.around(4*(ds['lat'].values+89.875 )).astype(np.int32) + 1 # idx start from 1 for fortran
            idx_lon = np.around(4*(ds['lon'].values+179.875)).astype(np.int32) + 1 # idx start from 1 for fortran           

            (daily_sla_avg, daily_sla_num) = fort.ssh_1dto2d_1day_1sat(ds['sla'].values, idx_lat, idx_lon)

            daily_sla_num = xr.where(landmask_oi==0, 0, daily_sla_num)  # mask land grid points
            daily_sla_avg = np.divide(daily_sla_avg, daily_sla_num, where=(daily_sla_num > 0.9))
            daily_sla_avg = xr.where(daily_sla_num==0, -32768, daily_sla_avg)           
            
            da_daily_sla_avg = xr.DataArray(data=np.float32(daily_sla_avg.T)  \
                , dims=['lat', 'lon'], coords={'lat': lat_oi, 'lon': lon_oi}, name='seaSurfaceHeightAnomaly'  \
                , attrs={'long_name':'daily sla', 'units':'m', '_FillValue':-32768})
            da_daily_sla_num = xr.DataArray(data=np.int8   (daily_sla_num[:, :].T)  \
                , dims=['lat', 'lon'], coords={'lat': lat_oi, 'lon': lon_oi}, name='ssha_num'  \
                , attrs=dict(_FillValue=0))

            ds_2d = xr.merge([da_daily_sla_avg, da_daily_sla_num])
        
            fn_2d = mi + '_' + str_date + '_' + p + '_2d.nc'
            ds_2d.to_netcdf(DIR_DATA + '/filtered_binToGrid/' + fn_2d 
                , encoding={'lat': {'_FillValue': None}, 'lon': {'_FillValue': None}}, format="NETCDF3_CLASSIC")

    jday += datetime.timedelta(days=1)


