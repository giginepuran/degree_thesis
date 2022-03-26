from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from lib.pyDriveLib import Get
from lib.pyDriveLib import Put
from lib.CommWithTaiwania import Transfer
import os
import time


def taiwania_work(population: int, max_generation: int, drive: GoogleDrive,
                  transfer_folder_id: str, local_transfer_folder: str):
    print('work flow settings:')
    print(f'max generation : {max_generation}')
    print(f'    population : {population}')
    print('-------------------------------------')
    print('Taiwania start working ...\n')

    mode_file_info = Get.get_file_info_by_subtitle(drive, transfer_folder_id, 'mode.txt')[0]
    fsp_info_list = Get.get_file_info_by_subtitle(drive, transfer_folder_id, '.fsp')
    if len(fsp_info_list) != population:
        print(f'number of fsp files is wrong\nActually number : {len(fsp_info_list)}\nExpected : {population}')
        return

    generation = 1
    while generation <= max_generation:
        print(f'Dealing with generation{generation}')
        print('-------------------------------------')

        print('Checking mode.txt ...')
        Transfer.keep_check_mode(mode_file_info, local_transfer_folder, 'doing_fdtd', period=30)

        print('Downloading *.fsp ...')
        drive = Transfer.refresh_drive_by_gauth()
        for fsp_info in fsp_info_list:
            Get.download_drive_file(drive, fsp_info, local_transfer_folder, move=True)

        print('Creating job script ...')
        split_number = create_job_script_split(local_transfer_folder, population, generation, 10)

        print('Doing qsub ...')
        #Transfer.qsub_fdtd_script(local_transfer_folder)
        qsub_fdtd_script(local_transfer_folder, split_number)

        print('Waiting job finished ...')
        #Transfer.check_qsub_finish(local_transfer_folder, population, print_step_msg=True)
        check_qsub_finish_split(local_transfer_folder, population, split_number, print_step_msg=True)

        print('Updating *.fsp to drive transfer folder ...')
        drive = Transfer.refresh_drive_by_gauth()
        if not Transfer.update_fsps(drive, transfer_folder_id, fsp_info_list, local_transfer_folder, population):
            return

        print('Updating mode.txt to drive transfer folder ...')
        drive = Transfer.refresh_drive_by_gauth()
        Transfer.change_mode_then_upload(drive, transfer_folder_id,
                                         mode_file_info, local_transfer_folder, 'building_fsp')

        print(f'calculating work of generation : {generation} finished!\n')
        generation = generation + 1



def check_qsub_finish_split(local_transfer_folder: str, population: int, split_number: int,
                            step=3600, print_step_msg=False):
    last_time = 0
    finish = False
    count = 0
    while not finish:
        checker = True
        for no in range(1, split_number+1):
            if not os.path.exists(f'{local_transfer_folder}/finish{no}.txt'):
                checker = False
        finish = checker
        if not finish:
            time.sleep(5 * population)
            last_time = last_time + population * 5
            if print_step_msg and last_time // step > count:
                count = last_time // step
                print(f'qsub is not finished yet, last time : {last_time}')
    print(f'fdtd job finished, last time : {last_time}')
    msg = os.popen(f'rm {local_transfer_folder}/qsub_script*.sh').read()
    msg = os.popen(f'rm {local_transfer_folder}/finish*.txt').read()
    msg = os.popen(f'mv *.o* ./local/job_output').read()


def qsub_fdtd_script(local_transfer_folder: str, split_number: int):
    for no in range(1, split_number+1):
        if no > 2:
            finish = False
            while not finish:
                if os.path.exists(f'{local_transfer_folder}/finish{no-2}.txt'):
                    finish = True
                else:
                    time.sleep(10)
        qsub_success = False
        while not qsub_success:
            job_id = os.popen(f'qsub {local_transfer_folder}/qsub_script{no}.sh').read()
            if ".srvc1" in job_id:
                print(f"job id : {job_id}")
                qsub_success = True
            else:
                print(f"qsub failed\nError message:{job_id}")
                time.sleep(5)


def create_job_script_split(local_transfer_folder: str, population: int, generation: int, max_fsp_in_a_job: int):
    if not (os.path.isdir(local_transfer_folder) and os.path.exists(f'./script/sh/fdtd_all_under_split.sh')):
        print('./script/sh/fdtd_all_under_split.sh not exists')
        return
    no = 1
    p = 1
    end = p + max_fsp_in_a_job - 1
    while p < population:
        with open(f'{local_transfer_folder}/qsub_script{no}.sh', "w") as txt:
            script = open('./script/sh/fdtd_all_under_split.sh', 'r').read()
            script = script.replace('{population}', f'{population}')
            script = script.replace('{generation}', f'{generation}')
            script = script.replace('{transfer_folder}', f'{local_transfer_folder}')
            script = script.replace('{start}', f'{p}')
            script = script.replace('{end}', f'{end if end < population else population}')
            script = script.replace('{no}', f'{no}')
            txt.write(script)
        no = no + 1
        p = p + max_fsp_in_a_job
        end = p + max_fsp_in_a_job - 1
    # number of job.sh
    return no - 1