#!/bin/bash
#PBS -P MST107345
#PBS -l walltime=2:00:00
#PBS -l select=4:ncpus=40:mpiprocs=40
#PBS -N Neff_Gen{generation}
#PBS -j oe
#PBS -M r09941007@g.ntu.edu.tw
#PBS -m abe
#PBS -q ct160
# ^PBS setting
# job
username=$"$USER"
module load intel/2018_u1
export I_MPI_HYDRA_BRANCH_COUNT=-1

# simulations through generation
# shellcheck disable=SC2164
cd /home/"$username"/result/optPath/Gen{generation}
# shellcheck disable=SC2043
for i in {1..{population}}
do
    # shellcheck disable=SC2164
    cd p"$i"
    mpiexec.hydra /home/"$username"/tools/lumerical/v212/bin/fdtd-engine-impi-lcl ind.fsp
    # shellcheck disable=SC2103
    cd ..
done
# generate finished sign in /home... bla bla bla
echo >>finish.txt

