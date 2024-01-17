'''
Description: Compute binned/average result on OI 0.25-degree grid from 0.02-degree ACSPO L3C daily SST.
    ACSPO L3C grid is the same as L3S, this script is modified from L3S script.
Author: Ligang Chen
Date created: 07/26/2022
Date last modified: 07/26/2022 
'''

import numpy as np
import xarray as xr

import os
import datetime
import glob
import struct


DIR = '/glade/p/univ/umcp0009/lgchen/data/OISSH_NOAA/fromEric/toIODA/dummyObs'
FN_RADS_ORG = "j2_2016100_org_RADS.nc"
ds = xr.open_dataset(filename_or_obj=DIR + '/' + FN_RADS_ORG, mask_and_scale=False
    , decode_times=False).head(1)
# print(ds)
ds['sla'][0] = 0
ds.to_netcdf(DIR+'/j2_2016100_RADS_1value.nc', encoding={'lat': {'_FillValue': None}, 'lon': {'_FillValue': None}})

