#!/usr/bin/env python3


import sys
import os
import datetime


# sats = ['c2', 'j2', 'sa']
# sats = ['j2', 'sa']
sats = ['j2', 'sa', 'j3', '3a']
jday_st = datetime.date(2016, 1, 1)
jday_end = datetime.date(2016, 12, 31)
dir_IODA_input = '/glade/p/univ/umcp0009/lgchen/data/OISSH_NOAA/fromEric/toIODA'
dir_link_output = '/glade/work/lgchen/project/OISSH_JEDI/OISSH_JEDI/generic-marine-jedi/cycling_ssh_2ndRun/obs'

for sat in sats:
    jday = jday_st
    while jday <= jday_end:
      # fdate = datetime.datetime.combine(jday, datetime.time(12))
        fn_in = sat + '_' + jday.strftime('%Y%j') + '.nc'
        fn_out = sat + '_' + jday.strftime('%Y%m%d') + '.nc'

        if os.path.isfile(dir_IODA_input + '/2016/' + fn_in):
          # str_cmd = 'ln -sf ' + dir_IODA_input + '/' + fn_in + ' ' + dir_link_output + '/' + fn_out
            os.symlink(dir_IODA_input + '/2016/' + fn_in, dir_link_output + '/' + fn_out)

        jday += datetime.timedelta(days=1)

