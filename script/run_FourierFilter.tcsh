#!/bin/tcsh

#PBS  -A UMCP0014   
#PBS  -l walltime=12:00:00              
# #PBS  -l select=1:ncpus=8:mpiprocs=8
# #PBS  -l select=1:ncpus=36:mpiprocs=36
#PBS  -l select=1:ncpus=1:mpiprocs=1 
#PBS  -N Fourier
#PBS  -j oe
#PBS  -q regular
 
python3 FourierFilter.py >&! FourierFilter_01.log
 
exit 0
