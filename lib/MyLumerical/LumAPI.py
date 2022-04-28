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


# std_y = 0.0403scale + 8E-08
def get_mode_mismatch_fom(fdtd: lumapi.FDTD, fsp_path: str):
    info = get_mode_profile_y(fdtd, fsp_path)
    size = info["p_of_y"].size
    sig = 0.0403 * info["scale"] + 8E-08
    t2 = get_transmission_wg2_fom(fdtd, fsp_path)  # enhance the weight of coupling efficiency
    gaussian_profile = gaussian(x=info["y"], mu=info["scale"]/2, sig=sig)
    fom = -tot_error_square(normalize(gaussian_profile), normalize(info["p_of_y"]))/size/(t2**2)
    return fom


def get_mode_profile_y(fdtd: lumapi.FDTD, fsp_path: str):
    if not os.path.exists(fsp_path):
        return -1
    success = False
    count_f = 0
    lsf_script = open('E:/degree_thesis/script/lsf/P_wg2_profile.lsf', 'r').read()
    result = {}
    while not success:
        try:
            fdtd.eval('newproject;')
            fdtd.load(fsp_path)
            fdtd.eval(lsf_script)
            result["p_of_y"] = fdtd.getv('PofY')
            result["y"] = fdtd.getv('y')
            result["scale"] = fdtd.getv('scale')
            fdtd.eval('newproject;')
            time.sleep(5)
            success = True
        except:
            count_f = count_f + 1
            print(f'Getting FOM failed, count = {count_f}')
            time.sleep(10)
    return result


def run_lsf_in_fdtd(fdtd: lumapi.FDTD, lsf_path: str):
    lsf_script = open(lsf_path, 'r').read()
    success = False
    count_f = 0
    while not success:
        try:
            fdtd.eval(lsf_script)
            time.sleep(1.5)
            success = True
        except:
            count_f = count_f + 1
            print(f'run lsf failed, count = {count_f}')
            time.sleep(10)


def get_value_from_fdtd(fdtd: lumapi.FDTD, para_name: str):
    success = False
    count_f = 0
    while not success:
        try:
            result = fdtd.getv(para_name)
            return result
        except:
            count_f = count_f + 1
            print(f'get value failed, count = {count_f}')
            time.sleep(10)


def gaussian(x, mu, sig):
    return np.exp((x - mu)*(x - mu) / (sig*sig) / 2)


def normalize(arr_in):
    factor = 1 / sum(arr_in)
    return arr_in * factor


def tot_error_square(curve, raw_data):
    err = curve - raw_data
    return sum(err * err)

