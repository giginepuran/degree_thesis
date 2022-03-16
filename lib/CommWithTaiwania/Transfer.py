from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from lib.pyDriveLib import Build
from lib.pyDriveLib import Get
from lib.pyDriveLib import Put
import os
import time


def keep_check_mode(drive:GoogleDrive, mode_file_info, local_transfer_folder: str, mode_msg: str, period=30):
    while True:
        Get.download_drive_file(drive, mode_file_info, dst=local_transfer_folder, move=True)
        mode = open(f'{local_transfer_folder}/mode.txt','r').read()
        if mode_msg in mode:
            break
        else:
            time.sleep(period)


def create_job_script(local_transfer_folder: str, population: int, generation: int):
    if not (os.path.isdir(local_transfer_folder) and os.path.exists(f'./script/sh/fdtd_all_under.sh')):
        print('./script/sh/fdtd_all_under.sh not exists')
        return
    with open(f'{local_transfer_folder}/qsub_script.sh', "w") as txt:
        script = open('./script/sh/fdtd_all_under.sh', 'r').read()
        script = script.replace('{population}', f'{population}')
        script = script.replace('{generation}', f'{generation}')
        script = script.replace('{transfer_folder}', f'{local_transfer_folder}')
        txt.write(script)


def qsub_fdtd_script(local_transfer_folder: str):
    qsub_success = False
    while not qsub_success:
        job_id = os.popen(f'qsub {local_transfer_folder}/qsub_script.sh').read()
        if ".srvc1" in job_id:
            print(f"job id : {job_id}")
            qsub_success = True
        else:
            print(f"qsub failed\nError message:{job_id}")
            time.sleep(5)


def check_qsub_finish(local_transfer_folder: str, population: int, step=60, print_step_msg=False):
    last_time = 0
    finish = False
    count = 0
    while not finish:
        if os.path.exists(f'{local_transfer_folder}/finish.txt'):
            finish = True
        else:
            time.sleep(5 * population)
            last_time = last_time + population * 5
            if print_step_msg and last_time // step > count:
                count = last_time // step
                print(f'qsub is not finished yet, last time : {last_time}')
    print(f'fdtd job finished, last time : {last_time}')
    msg = os.popen(f'rm {local_transfer_folder}/qsub_script.sh').read()
    msg = os.popen(f'rm {local_transfer_folder}/finish.txt').read()


def update_fsps(drive:GoogleDrive, parent_id: str, file_info_list: list, local_transfer_folder: str, population: int):
    suc_num = 0
    for file_info in file_info_list:
        title = file_info['title']
        if '.fsp' not in title:
            continue
        if Put.update_file(drive, parent_id, file_info, f'{local_transfer_folder}/{title}'):
            suc_num = suc_num + 1
    if suc_num != population:
        print(f'number of fsp files uploaded is wrong\nActually number : {suc_num}\nExpected : {population}')
        return False
    return True


def change_mode_then_upload(drive: GoogleDrive, parent_id: str, mode_file_info, local_transfer_folder: str, mode_msg: str):
    msg = os.popen(f'echo {mode_msg} > {local_transfer_folder}/mode.txt').read()
    Put.update_file(drive, parent_id, mode_file_info, f'{local_transfer_folder}/mode.txt')
