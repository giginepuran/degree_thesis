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
            for particle in range(1, population + 1):
                os.mkdir(f'{saving_path}/Gen{gen}/p{particle}')
                os.mkdir(f'{saving_path}/Gen{gen}/p{particle}/pbest')
    except:
        return False
    return True


