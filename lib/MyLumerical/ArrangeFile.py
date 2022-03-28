import os
import shutil
import sys
import lumapi
from past.builtins import execfile
import time
from os.path import exists
from lib.PSO import swarm


def build_saving_path(saving_path: str, max_generation: int, population: int):
    if not os.path.isdir(saving_path):
        print(f'saving path error, can not find directory {saving_path}')
        return False
    try:
        for gen in range(1, max_generation + 1):
            os.mkdir(f'{saving_path}/Gen{gen}')
            os.mkdir(f'{saving_path}/Gen{gen}/gbest')
            for p_no in range(1, population + 1):
                os.mkdir(f'{saving_path}/Gen{gen}/p{p_no}')
                os.mkdir(f'{saving_path}/Gen{gen}/p{p_no}/pbest')
    except:
        return False
    return True


def move_fsp_to_saving_path(local_transfer_folder: str, saving_path: str, generation: int, p_no: int):
    shutil.move(f'{local_transfer_folder}/ind{p_no}.fsp', f'{saving_path}/Gen{generation}/p{p_no}/ind{p_no}.fsp')


def copy_particle_to_pbest_overwrite(saving_path: str, generation: int, p_no: int, dimension: int):
    shutil.copy(f'{saving_path}/Gen{generation}/p{p_no}/ind{p_no}.fsp',
                f'{saving_path}/Gen{generation}/p{p_no}/pbest/ind{p_no}.fsp')
    shutil.copy(f'{saving_path}/Gen{generation}/p{p_no}/fom.txt',
                f'{saving_path}/Gen{generation}/p{p_no}/pbest/fom.txt')
    for d in range(1, dimension+1):
        shutil.copy(f'{saving_path}/Gen{generation}/p{p_no}/para{d}.txt',
                    f'{saving_path}/Gen{generation}/p{p_no}/pbest/para{d}.txt')


def inherit_pbest_to_next_generation(saving_path: str, current_generation: int, population: int, dimension: int):
    for p_no in range(1, population+1):
        shutil.copy(f'{saving_path}/Gen{current_generation}/p{p_no}/pbest/ind{p_no}.fsp',
                    f'{saving_path}/Gen{current_generation+1}/p{p_no}/pbest/ind{p_no}.fsp')
        shutil.copy(f'{saving_path}/Gen{current_generation}/p{p_no}/pbest/fom.txt',
                    f'{saving_path}/Gen{current_generation+1}/p{p_no}/pbest/fom.txt')
        for d in range(1, dimension + 1):
            shutil.copy(f'{saving_path}/Gen{current_generation}/p{p_no}/pbest/para{d}.txt',
                        f'{saving_path}/Gen{current_generation+1}/p{p_no}/pbest/para{d}.txt')


def copy_pbest_to_gbest_overwrite(saving_path: str, generation: int, pbest_p_no: int, dimension: int):
    shutil.copy(f'{saving_path}/Gen{generation}/p{pbest_p_no}/pbest/ind{pbest_p_no}.fsp',
                f'{saving_path}/Gen{generation}/gbest/ind{pbest_p_no}.fsp')
    shutil.copy(f'{saving_path}/Gen{generation}/p{pbest_p_no}/pbest/fom.txt',
                f'{saving_path}/Gen{generation}/gbest/fom.txt')
    for d in range(1, dimension+1):
        shutil.copy(f'{saving_path}/Gen{generation}/p{pbest_p_no}/pbest/para{d}.txt',
                    f'{saving_path}/Gen{generation}/gbest/para{d}.txt')

