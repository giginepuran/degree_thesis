import os
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


def get_fom(fdtd: lumapi.FDTD, lsf_script: str, fsp_path: str):
    if not os.path.exists(fsp_path):
        return -1
    success = False
    count_f = 0
    while not success:
        try:
            fdtd.eval('newproject;')
            fdtd.load(fsp_path)
            fdtd.eval(lsf_script)
            result = fdtd.getv('FOM')
            fdtd.eval('newproject;')
            time.sleep(5)
            success = True
        except:
            count_f = count_f + 1
            print(f'Getting FOM failed, count = {count_f}')
            time.sleep(10)
    return result


def get_mode_profile_y(fdtd: lumapi.FDTD, fsp_path: str):
    if not os.path.exists(fsp_path):
        return -1
    success = False
    count_f = 0
    lsf_script = open('E:/degree_thesis/script/lsf/P_wg2_far_profile.lsf', 'r').read()
    result = {}
    while not success:
        try:
            fdtd.eval('newproject;')
            fdtd.load(fsp_path)
            fdtd.eval(lsf_script)
            result["p_of_y"] = fdtd.getv('PofY')
            result["y"] = fdtd.getv('y')
            fdtd.eval('newproject;')
            time.sleep(5)
            success = True
        except:
            count_f = count_f + 1
            print(f'Getting FOM failed, count = {count_f}')
            time.sleep(10)
    return result

