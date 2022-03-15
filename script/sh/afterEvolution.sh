#!/bin/bash

username=$"$USER"
cd /home/"$username"/result/optPath/Gen{generation}
for i in {1..{population}}
do
    # shellcheck disable=SC2164
    cd p"$i"
    rm ind.fsp
    cd pbest
    rm ind.fsp
    cd ..
    cd ..
done
