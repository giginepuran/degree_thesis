import shutil
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from lib.pyDriveLib import Build
from lib.pyDriveLib import Get
from lib.pyDriveLib import Put
from lib.CommWithTaiwania import Transfer
import os
import time
from lib.PSO import swarm
from lib.PSO import particle


def build_work(population: int, max_generation: int, drive: GoogleDrive,
               transfer_folder_id: str, local_transfer_folder: str,
               dimension: int, floor: list, ceiling: list, saving_path: str):
    print('Initializing transfer folder on google drive ...')
    initialize_drive_transfer_folder(drive, transfer_folder_id, population)

    print('work flow settings:')
    print(f'max generation : {max_generation}')
    print(f'    population : {population}')
    print('-------------------------------------')
    print('Generating swarm ...')
    my_swarm = swarm.Swarm(dimension, population, floor, ceiling)
    print('opening fdtd gui ...')
    # fdtd = lumapi.FDTD(hide=True)
    print('loading lsf script ...')
    setBase = open('./script/lsf/setBase1.lsf', 'r').read()
    getData = open('./script/lsf/getData.lsf', 'r').read()
    print(f'Getting ids of mode_file and fsp_list ...')
    mode_file_info = Get.get_file_info_by_subtitle(drive, transfer_folder_id, 'mode.txt', all_folder=False)[0]
    fsp_info_list = Get.get_file_info_by_subtitle(drive, transfer_folder_id, '.fsp', all_folder=False)
    if len(fsp_info_list) != population:
        print(f'number of fsp files is wrong\nActually number : {len(fsp_info_list)}\nExpected : {population}')
        return

    print('Build host start working ...\n')
    generation = 1
    while generation <= max_generation:
        print(f'Dealing with generation{generation}')
        print('-------------------------------------')

        print('Building fsp ...')
        build_fsps(population, local_transfer_folder)

        print('Recording parameters ...')

        print('Updating *.fsp to drive transfer folder ...')
        if not Transfer.update_fsps(drive, transfer_folder_id, fsp_info_list, local_transfer_folder, population):
            return

        print('Updating mode.txt to drive transfer folder ...')
        Transfer.change_mode_then_upload(drive, transfer_folder_id, mode_file_info, local_transfer_folder, 'doing_fdtd')

        print('Checking mode.txt ...')
        Transfer.keep_check_mode(drive, mode_file_info, local_transfer_folder, 'building_fsp', period=30)

        print('Downloading *.fsp ...')
        for fsp_info in fsp_info_list:
            Get.download_drive_file(drive, fsp_info, dst=local_transfer_folder, move=True)

        print('Collecting data from *.fsp ...')

        print('Recording data to saving path ...')

        print('Saving *.fsp to saving path ...')

        print('Selecting pbest ...')

        print('Selecting gbest ...')

        print('Particles evolving ...')
        # my_swarm.evolution()

        generation = generation + 1


def initialize_drive_transfer_folder(drive: GoogleDrive, transfer_folder_id: str, population: int):
    file_list = drive.ListFile({'q': f"'{transfer_folder_id}' in parents and trashed=false"}).GetList()
    for file in file_list:
        file.Delete()
    for i in range(1, population+1):
        Put.create_file_to_id(drive, transfer_folder_id, './local/ind_template.fsp',
                              change_name=True, put_name=f'ind{i}.fsp')


def build_saving_path():
    return


def build_fsps(population: int, local_transfer_folder: str):
    # temporary
    for i in range(1, population+1):
        shutil.copy('./local/ind_template.fsp', f'{local_transfer_folder}/ind{i}.fsp')


def record_parameters():
    return


def collect_data():
    return


def record_data():
    return


def save_to_saving_path():
    return


def select_pbest():
    return


def select_gbest():
    return


