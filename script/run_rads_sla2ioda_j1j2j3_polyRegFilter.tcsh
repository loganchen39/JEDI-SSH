#!/bin/bash
# #!/bin/tcsh

#PBS  -A UMCP0014   
#PBS  -l walltime=12:00:00              
# #PBS  -l select=1:ncpus=36:mpiprocs=36
#PBS  -l select=1:ncpus=1:mpiprocs=1 
#PBS  -N rads2ioda_j2_2008-2013
#PBS  -j oe
#PBS  -q main
#PBS -M lchen2@umd.edu

module load conda/latest
conda activate npl
 
# ./rads_sla2ioda_01.py -s 20000101 -e 20221231 -i /glade/scratch/lgchen/data/OISSH_NOAA/2000-2022_fromEric/link -o /glade/scratch/lgchen/data/OISSH_NOAA/2000-2022_fromEric/toIODA >&! rads_sla2ioda_01_11.log

./rads_sla2ioda_j1j2j3_polyRegFilter.py -s 20080101 -e 20131231 -i /glade/u/home/lgchen/umcp0014/lgchen/OISSH_JEDI_DATA/2000-2022_fromEric/polyRegFilter/filtered -o /glade/u/home/lgchen/umcp0014/lgchen/OISSH_JEDI_DATA/2000-2022_fromEric/polyRegFilter/filtered_toIODA
 
exit 0
