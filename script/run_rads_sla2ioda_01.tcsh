#!/bin/tcsh

# #PBS  -A UMCP0009   
#PBS  -A UMCP0014   
#PBS  -l walltime=12:00:00              
# #PBS  -l select=1:ncpus=36:mpiprocs=36
#PBS  -l select=1:ncpus=1:mpiprocs=1 
#PBS  -N 01_rads2ioda
#PBS  -j oe
#PBS  -q economy
 
./rads_sla2ioda_01.py -s 20000101 -e 20221231 -i /glade/scratch/lgchen/data/OISSH_NOAA/2000-2022_fromEric/link -o /glade/scratch/lgchen/data/OISSH_NOAA/2000-2022_fromEric/toIODA >&! rads_sla2ioda_01_11.log
 
exit 0
