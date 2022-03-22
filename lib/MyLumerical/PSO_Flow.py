import os
import shutil
import sys

import past.builtins

import lumapi
from past.builtins import execfile
import time
import numpy as np
from scipy.interpolate import interp1d
from os.path import exists
from lib.PSO import swarm
from lib.MyLumerical import LumAPI
from lib.MyLumerical import ArrangeFile
from lib.PSO import swarm
from lib.PSO import particle


def step1_initialize_saving_path(saving_path: str, max_generation: int, population: int):
    if ArrangeFile.build_saving_path(saving_path, max_generation, population):
        return 0
    return -1


def step2_create_swarm(dimension: int, population: int, floor: list, ceiling: list):
    return swarm.Swarm(dimension, population, floor, ceiling)


def step3_build_fsp_by_swarm(fdtd: lumapi.FDTD, my_swarm: swarm.Swarm, build_lsf: str,
                             local_transfer_folder: str, dimension: int, population: int):
    if not os.path.isdir(local_transfer_folder):
        return -1
    if not os.path.exists(build_lsf):
        return -1
    for p in range(1, population+1):
        para = my_swarm.particles[p-1].get_x()
        build_script = open(f'{build_lsf}', 'r').read()
        for i in range(1, dimension + 1, 1):
            build_script = build_script.replace(f'para{i}__', f'{round(para[i - 1][0], 2)}')
        build_script = build_script.replace('__save_to__', f'{local_transfer_folder}/ind{p}.fsp')
        LumAPI.build_fsp(fdtd, build_script)
        # after building, fdtd need time to release resource.
        # Otherwise, it will build very very slow...
        time.sleep(10)
    return 0


# between step 3 and step 4, we need to
# 1. upload the latest fsp files
# 2. waiting simulation on taiwania finished
# 3. download the fsp files with data to build host
def step4_get_fom_of_each_particle(fdtd: lumapi.FDTD, get_data_lsf: str, population: int, local_transfer_folder: str):
    fom = []
    get_data_script = open(f'{get_data_lsf}', 'r').read()
    for p in range(1, population+1):
        result = LumAPI.get_fom(fdtd, get_data_script, f'{local_transfer_folder}/ind{p}.fsp')
        fom.append(result)
    return fom


def step5_update_fom_to_swarm(my_swarm: swarm.Swarm, fom: list):
    # pbest_changed is a list of boolean, True if latest fom greater than pbest, otherwise False
    pbest_changed = my_swarm.update_fom(fom)
    return pbest_changed


def step6_saving_fsp_to_saving_path(local_transfer_folder: str, saving_path:str, generation: int, population: int):
    for p_no in range(1, population+1):
        ArrangeFile.move_fsp_to_saving_path(local_transfer_folder, saving_path, generation, p_no)


def step7_recording_parameters_and_fom_of_each_particle(saving_path: str, my_swarm: swarm.Swarm,
                                                        generation: int, population: int, dimension: int):
    for p in range(1, population+1):
        with open(f'{saving_path}/Gen{generation}/p{p}/fom.txt', "w") as txt:
            txt.write(f'{my_swarm.particles[p-1].get_fom()}')
        for d in range(1, dimension+1):
            with open(f'{saving_path}/Gen{generation}/p{p}/para{d}.txt', "w") as txt:
                txt.write(f'{my_swarm.xs[p-1][d-1][0]}')


def step8_update_pbest_of_each_particle(saving_path: str, pbest_changed: list, generation: int, dimension: int):
    for p_no in range(1, len(pbest_changed)+1):
        if pbest_changed[p_no-1]:
            ArrangeFile.copy_particle_to_pbest_overwrite(saving_path, generation, p_no, dimension)


def step9_select_gbest_from_pbest(saving_path: str, pbest_p_no, generation: int, dimension: int):
    ArrangeFile.copy_pbest_to_gbest_overwrite(saving_path, generation, pbest_p_no, dimension)


def step10_inherit_pbest_to_next_generation(saving_path: str, current_generation, population, dimension):
    ArrangeFile.inherit_pbest_to_next_generation(saving_path, current_generation, population, dimension)


def interpolation_by_swarm(particle_x: np.ndarray, dimension: int, parameter_num: int,
                           interpol_point_num: int, interpol_start: int, interpol_end: int):
    after_interpolation = []
    num_of_point_in_a_set = dimension // parameter_num
    for para_no in range(1, parameter_num+1):
        x = np.linspace(interpol_start, interpol_end, num=num_of_point_in_a_set, endpoint=True)
        y = particle_x[(para_no-1)*parameter_num:para_no*parameter_num]
        f = interp1d(x, y.reshape(parameter_num,), kind='cubic')
        x_new = np.linspace(interpol_start, interpol_end, num=interpol_point_num, endpoint=True)
        after_interpolation.append(f(x_new))
    return after_interpolation


def step3_build_fsp_by_swarm_interpolation(fdtd: lumapi.FDTD, my_swarm: swarm.Swarm, build_lsf: str,
                                           local_transfer_folder: str, dimension: int, population: int,
                                           parameter_num: int):
    if not os.path.isdir(local_transfer_folder):
        return -1
    if not os.path.exists(build_lsf):
        return -1
    for p in range(1, population+1):
        parameters = interpolation_by_swarm(my_swarm.particles[p-1].get_x(), dimension, parameter_num, 20, 1, 20)
        build_script = open(f'{build_lsf}', 'r').read()
        for para_no in range(1, parameter_num+1):
            set_of_para = parameters[para_no-1]
            for para_no_no in range(1, 20+1):
                build_script = build_script.replace(f'para{para_no}__{para_no_no}',
                                                    f'{round(set_of_para[para_no_no - 1], 2)}')
        build_script = build_script.replace('__save_to__', f'{local_transfer_folder}/ind{p}.fsp')
        LumAPI.build_fsp(fdtd, build_script)
        # after building, fdtd need time to release resource.
        # Otherwise, it will build very very slow...
        time.sleep(10)


