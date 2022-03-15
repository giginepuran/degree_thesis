#!/bin/bash
#PBS -P MST107345
#PBS -l walltime=00:10:00
#PBS -l select=1:ncpus=40:mpiprocs=40
#PBS -N Neff_Gen{generation}
#PBS -j oe
#PBS -M r09941007@g.ntu.edu.tw
#PBS -m abe
#PBS -q ctest
# ^PBS setting
# job

module load intel/2018_u1
export I_MPI_HYDRA_BRANCH_COUNT=-1

# simulations all under
cd {transfer_folder}
for i in {1..{population}}
do
    mpiexec.hydra /home/u6097335/tools/lumerical/v212/bin/fdtd-engine-impi-lcl ind"$i".fsp
done
# finish.txt will save under folder same as *fsp
echo >> finish.txt

