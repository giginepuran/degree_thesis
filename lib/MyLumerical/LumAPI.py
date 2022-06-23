import os
import numpy as np
import lumapi
import time


def build_fsp(fdtd: lumapi.FDTD, script: str):
    success = False
    count_f = 0
    while not success:
        try:
            fdtd.eval(script)
            success = True
        except:
            count_f = count_f + 1
            print(f'Building failed, count = {count_f}')
            time.sleep(10)
    return success


def get_transmission_wg2_fom(fdtd: lumapi.FDTD, fsp_path: str):
    if not os.path.exists(fsp_path):
        return -1
    success = False
    count_f = 0
    lsf_script = open('E:/degree_thesis/script/lsf/T_P_wg2.lsf', 'r').read()
    while not success:
        try:
            fdtd.eval('newproject;')
            fdtd.load(fsp_path)
            fdtd.eval(lsf_script)
            fom = fdtd.getv('T2')
            fdtd.eval('newproject;')
            time.sleep(5)
            success = True
        except:
            count_f = count_f + 1
            print(f'Getting FOM failed, count = {count_f}')
            time.sleep(10)
    return fom


def get_transmission_wg2_far_fom(fdtd: lumapi.FDTD, fsp_path: str):
    if not os.path.exists(fsp_path):
        return -1
    success = False
    count_f = 0
    lsf_script = open('E:/degree_thesis/script/lsf/T_P_wg2_far.lsf', 'r').read()
    while not success:
        try:
            fdtd.eval('newproject;')
            fdtd.load(fsp_path)
            fdtd.eval(lsf_script)
            fom = fdtd.getv('T2')
            fdtd.eval('newproject;')
            time.sleep(5)
            success = True
        except:
            count_f = count_f + 1
            print(f'Getting FOM failed, count = {count_f}')
            time.sleep(10)
    return fom


def get_mode_expansion_t_wg2_fom(fdtd: lumapi.FDTD, fsp_path: str):
    if not os.path.exists(fsp_path):
        return -1
    success = False
    count_f = 0
    lsf_script = open('E:/degree_thesis/script/lsf/t_expansion_P_wg2.lsf', 'r').read()
    while not success:
        try:
            fdtd.eval('newproject;')
            fdtd.load(fsp_path)
            fdtd.eval(lsf_script)
            fom = fdtd.getv('FOM')
            fdtd.eval('newproject;')
            time.sleep(5)
            success = True
        except:
            count_f = count_f + 1
            print(f'Getting FOM failed, count = {count_f}')
            time.sleep(10)
    return fom


def get_mode_expansion_fraction_wg2_fom(fdtd: lumapi.FDTD, fsp_path: str):
    if not os.path.exists(fsp_path):
        return -1
    success = False
    count_f = 0
    lsf_script = open('E:/degree_thesis/script/lsf/expansion_P_wg2_fraction.lsf', 'r').read()
    while not success:
        try:
            fdtd.eval('newproject;')
            fdtd.load(fsp_path)
            fdtd.eval(lsf_script)
            fom = fdtd.getv('FOM')
            fdtd.eval('newproject;')
            time.sleep(5)
            success = True
        except:
            count_f = count_f + 1
            print(f'Getting FOM failed, count = {count_f}')
            time.sleep(10)
    return fom


def get_mode_expansion_fraction_wg2_far_fom(fdtd: lumapi.FDTD, fsp_path: str):
    if not os.path.exists(fsp_path):
        return -1
    success = False
    count_f = 0
    lsf_script = open('E:/degree_thesis/script/lsf/expansion_P_wg2_far_fraction.lsf', 'r').read()
    while not success:
        try:
            fdtd.eval('newproject;')
            fdtd.load(fsp_path)
            fdtd.eval(lsf_script)
            fom = fdtd.getv('FOM')
            fdtd.eval('newproject;')
            time.sleep(5)
            success = True
        except:
            count_f = count_f + 1
            print(f'Getting FOM failed, count = {count_f}')
            time.sleep(10)
    return fom

def run_lsf_in_fdtd(fdtd: lumapi.FDTD, lsf_path: str):
    lsf_script = open(lsf_path, 'r').read()
    fdtd.eval(lsf_script)


def get_value_from_fdtd(fdtd: lumapi.FDTD, para_name: str):
    result = fdtd.getv(para_name)
    return result