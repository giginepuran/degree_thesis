import os
import shutil
import sys
import lumapi
from past.builtins import execfile
import time
from os.path import exists
from lib.PSO import swarm


def build_fsp(fdtd: lumapi.FDTD, lsf_script: str, save_to: str, file_name: str):
    if not os.path.isdir(save_to):
        return False
    success = False
    count_f = 0
    while not success:
        try:
            fdtd.eval(lsf_script)
            fdtd.save(f'{save_to}/{file_name}')
            success = True
        except:
            count_f = count_f + 1
            print(f'Building failed, count = {count_f}')
            time.sleep(10)
    fdtd = lumapi.FDTD()
    return success


def get_fom(fdtd: lumapi.FDTD, lsf_script: str, fsp_path: str):
    if not os.path.exists(fsp_path):
        return -1
    success = False
    count_f = 0
    while not success:
        try:
            fdtd.load(fsp_path)
            fdtd.eval(lsf_script)
            result = fdtd.getv('FOM')
            success = True
        except:
            count_f = count_f + 1
            print(f'Getting FOM failed, count = {count_f}')
            time.sleep(10)
    fdtd = lumapi.FDTD()
    return result
