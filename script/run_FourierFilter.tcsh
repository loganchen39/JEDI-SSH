#!/bin/tcsh

#PBS  -A UMCP0014   
#PBS  -l walltime=12:00:00              
# #PBS  -l select=1:ncpus=8:mpiprocs=8
# #PBS  -l select=1:ncpus=36:mpiprocs=36
#PBS  -l select=1:ncpus=1:mpiprocs=1 
#PBS  -N Fourier
#PBS  -j oe
#PBS  -q main
#PBS -M lchen2@umd.edu


module load conda
conda activate npl

python3 FourierFilter.py >&! FourierFilter_03.log
 
exit 0
