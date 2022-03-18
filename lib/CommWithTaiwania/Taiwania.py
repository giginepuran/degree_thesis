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
        Transfer.create_job_script(local_transfer_folder, population, generation)

        print('Doing qsub ...')
        Transfer.qsub_fdtd_script(local_transfer_folder)

        print('Waiting job finished ...')
        Transfer.check_qsub_finish(local_transfer_folder, population, print_step_msg=True)

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


