from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pyDriveLib import Build
from pyDriveLib import Get
from pyDriveLib import Put
from py import Transfer
import os
import time


def taiwania_work(population: int, max_generation: int, drive: GoogleDrive,
                  transfer_folder_id: str, local_transfer_folder: str):
    print('work flow settings:')
    print(f'max generation : {max_generation}')
    print(f'    population : {population}')
    print('-------------------------------------')
    print('Taiwania start working ...\n')

    mode_file = Get.get_drive_file_by_subtitle(drive, transfer_folder_id, 'mode.txt', all_folder=False)[0]
    fsp_list = Get.get_drive_file_by_subtitle(drive, transfer_folder_id, '.fsp', all_folder=False)
    if len(fsp_list) != population:
        print(f'number of fsp files is wrong\nActually number : {len(fsp_list)}\nExpected : {population}')
        return

    generation = 1
    while generation <= max_generation:
        print(f'Dealing with generation{generation}')
        print('-------------------------------------')

        print('Checking mode.txt ...')
        Transfer.keep_check_mode(mode_file, local_transfer_folder, 'doing_fdtd', period=30)

        print('Downloading *.fsp ...')
        for fsp_file in fsp_list:
            Get.download_drive_file(fsp_file, local_transfer_folder)

        print('Creating job script ...')
        Transfer.create_job_script(local_transfer_folder, 2, generation)

        print('Doing qsub ...')
        Transfer.qsub_fdtd_script(local_transfer_folder)

        print('Waiting job finished ...')
        Transfer.check_qsub_finish(local_transfer_folder, population, print_step_msg=True)

        print('Updating *.fsp to drive transfer folder ...')
        act_num = Transfer.update_fsps(fsp_list, local_transfer_folder)
        if act_num != population:
            print(f'number of fsp files uploaded is wrong\nActually number : {act_num}\nExpected : {population}')
            return

        print('Updating mode.txt to drive transfer folder ...')
        Transfer.change_mode_then_upload(mode_file, local_transfer_folder, 'building_fsp')

        print(f'calculating work of generation : {generation} finished!\n')
        generation = generation + 1






