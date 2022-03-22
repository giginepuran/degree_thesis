import shutil
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from lib.pyDriveLib import Get
from lib.pyDriveLib import Put
from lib.CommWithTaiwania import Transfer
import os
import time
import lumapi
from lib.PSO import swarm
from lib.PSO import particle
from lib.MyLumerical import PSO_Flow


def build_work(population: int, max_generation: int, drive: GoogleDrive,
               transfer_folder_id: str, local_transfer_folder: str,
               dimension: int, floor: list, ceiling: list, saving_path: str):
    print('PSO settings:')
    print(f'local transfer folder : {local_transfer_folder}')
    print(f'          saving path : {saving_path}')
    print(f'       max generation : {max_generation}')
    print(f'           population : {population}')
    print(f'            dimension : {dimension}')
    print('-------------------------------------')

    print('initializing saving path ...')
    if PSO_Flow.step1_initialize_saving_path(saving_path, max_generation, population) == -1:
        return

    print('opening fdtd gui ...')
    fdtd = lumapi.FDTD(hide=False)

    print('Creating swarm ...')
    my_swarm = PSO_Flow.step2_create_swarm(dimension, population, floor, ceiling)

    print(f'Getting ids of mode_file and fsp_list ...')
    mode_file_info = Get.get_file_info_by_subtitle(drive, transfer_folder_id, 'mode.txt', all_folder=False)[0]
    fsp_info_list = Get.get_file_info_by_subtitle(drive, transfer_folder_id, '.fsp', all_folder=False)
    if len(fsp_info_list) != population:
        print(f'number of fsp files is wrong\nActually number : {len(fsp_info_list)}\nExpected : {population}')
        return

    print('Build host start working ...\n')
    generation = 1
    while generation <= max_generation:
        print(f'Building with generation{generation}')
        print('-------------------------------------')

        print('Building fsp ...')
        PSO_Flow.step3_build_fsp_by_swarm(fdtd, my_swarm, './script/lsf/setBase2.lsf',
                                          local_transfer_folder, dimension, population)

        print('Updating *.fsp to drive transfer folder ...')
        drive = Transfer.refresh_drive_by_gauth()
        if not Transfer.update_fsps(drive, transfer_folder_id, fsp_info_list, local_transfer_folder, population):
            return

        print('Updating mode.txt to drive transfer folder ...')
        drive = Transfer.refresh_drive_by_gauth()
        Transfer.change_mode_then_upload(drive, transfer_folder_id, mode_file_info, local_transfer_folder, 'doing_fdtd')

        print('Checking mode.txt ...')
        Transfer.keep_check_mode(mode_file_info, local_transfer_folder, 'building_fsp', period=30)

        print('Downloading *.fsp ...')
        drive = Transfer.refresh_drive_by_gauth()
        for fsp_info in fsp_info_list:
            Get.download_drive_file(drive, fsp_info, dst=local_transfer_folder, move=True)

        print('Collecting data from *.fsp ...')
        fom = PSO_Flow.step4_get_fom_of_each_particle(fdtd, './script/lsf/getData.lsf',
                                                      population, local_transfer_folder)

        print('Updating fom of each particle to swarm ...')
        pbest_changed = PSO_Flow.step5_update_fom_to_swarm(my_swarm, fom)

        print('Saving *.fsp to saving path ...')
        PSO_Flow.step6_saving_fsp_to_saving_path(local_transfer_folder, saving_path, generation, population)

        print('Saving parameters and fom of each particle to saving path ...')
        PSO_Flow.step7_recording_parameters_and_fom_of_each_particle(saving_path, my_swarm,
                                                                     generation, population, dimension)

        print('Updating files of pbest of each particle, if it should do ...')
        PSO_Flow.step8_update_pbest_of_each_particle(saving_path, pbest_changed, generation, dimension)

        print('Selecting gbest ...')
        PSO_Flow.step9_select_gbest_from_pbest(saving_path, my_swarm.gbest_index+1, generation, dimension)

        print('Putting pbest to next generation ...')
        if generation != max_generation:
            PSO_Flow.step10_inherit_pbest_to_next_generation(saving_path, generation, population, dimension)

        print('Particles evolving ...')
        my_swarm.evolution()

        print(f'Saving data of generation {generation} finished!\n')
        generation = generation + 1


def initialize_drive_transfer_folder(drive: GoogleDrive, transfer_folder_id: str, population: int):
    file_list = drive.ListFile({'q': f"'{transfer_folder_id}' in parents and trashed=false"}).GetList()
    for file in file_list:
        drive.CreateFile({'id': file['id']}).Delete()
    for i in range(1, population+1):
        Put.create_file_to_id(drive, transfer_folder_id, './local/ind_template.fsp',
                              change_name=True, put_name=f'ind{i}.fsp')
    Put.create_file_to_id(drive, transfer_folder_id, './local/mode_template.txt',
                          change_name=True, put_name='mode.txt')


def build_fsps(population: int, local_transfer_folder: str):
    # temporary
    for i in range(1, population+1):
        shutil.copy('./local/ind_template.fsp', f'{local_transfer_folder}/ind{i}.fsp')


def build_work_interpolation(population: int, max_generation: int, drive: GoogleDrive,
                             transfer_folder_id: str, local_transfer_folder: str,
                             dimension: int, floor: list, ceiling: list, saving_path: str):
    print('PSO settings:')
    print(f'local transfer folder : {local_transfer_folder}')
    print(f'          saving path : {saving_path}')
    print(f'       max generation : {max_generation}')
    print(f'           population : {population}')
    print(f'            dimension : {dimension}')
    print('-------------------------------------')

    print('initializing saving path ...')
    PSO_Flow.step1_initialize_saving_path(saving_path, max_generation, population)
    #if PSO_Flow.step1_initialize_saving_path(saving_path, max_generation, population) == -1:
    #    return

    print('opening fdtd gui ...')
    fdtd = lumapi.FDTD(hide=False)

    print('Creating swarm ...')
    my_swarm = PSO_Flow.step2_create_swarm(dimension, population, floor, ceiling)

    print(f'Getting ids of mode_file and fsp_list ...')
    mode_file_info = Get.get_file_info_by_subtitle(drive, transfer_folder_id, 'mode.txt', all_folder=False)[0]
    fsp_info_list = Get.get_file_info_by_subtitle(drive, transfer_folder_id, '.fsp', all_folder=False)
    if len(fsp_info_list) != population:
        print(f'number of fsp files is wrong\nActually number : {len(fsp_info_list)}\nExpected : {population}')
        return

    print('Build host start working ...\n')
    generation = 1
    while generation <= max_generation:
        print(f'Building with generation{generation}')
        print('-------------------------------------')

        print('Building fsp ...')
        PSO_Flow.step3_build_fsp_by_swarm_interpolation(fdtd, my_swarm, 'E:/degree_thesis/script/lsf/setBase3.lsf',
                                                        local_transfer_folder, dimension, population, 5)

        print('Updating *.fsp to drive transfer folder ...')
        drive = Transfer.refresh_drive_by_gauth()
        if not Transfer.update_fsps(drive, transfer_folder_id, fsp_info_list, local_transfer_folder, population):
            return

        print('Updating mode.txt to drive transfer folder ...')
        drive = Transfer.refresh_drive_by_gauth()
        Transfer.change_mode_then_upload(drive, transfer_folder_id, mode_file_info, local_transfer_folder, 'doing_fdtd')

        print('Checking mode.txt ...')
        Transfer.keep_check_mode(mode_file_info, local_transfer_folder, 'building_fsp', period=30)

        print('Downloading *.fsp ...')
        drive = Transfer.refresh_drive_by_gauth()
        for fsp_info in fsp_info_list:
            Get.download_drive_file(drive, fsp_info, dst=local_transfer_folder, move=True)

        print('Collecting data from *.fsp ...')
        fom = PSO_Flow.step4_get_fom_of_each_particle(fdtd, './script/lsf/getData.lsf',
                                                      population, local_transfer_folder)

        print('Updating fom of each particle to swarm ...')
        pbest_changed = PSO_Flow.step5_update_fom_to_swarm(my_swarm, fom)

        print('Saving *.fsp to saving path ...')
        PSO_Flow.step6_saving_fsp_to_saving_path(local_transfer_folder, saving_path, generation, population)

        print('Saving parameters and fom of each particle to saving path ...')
        PSO_Flow.step7_recording_parameters_and_fom_of_each_particle(saving_path, my_swarm,
                                                                     generation, population, dimension)

        print('Updating files of pbest of each particle, if it should do ...')
        PSO_Flow.step8_update_pbest_of_each_particle(saving_path, pbest_changed, generation, dimension)

        print('Selecting gbest ...')
        PSO_Flow.step9_select_gbest_from_pbest(saving_path, my_swarm.gbest_index+1, generation, dimension)

        print('Putting pbest to next generation ...')
        if generation != max_generation:
            PSO_Flow.step10_inherit_pbest_to_next_generation(saving_path, generation, population, dimension)

        print('Particles evolving ...')
        my_swarm.evolution()

        print(f'Saving data of generation {generation} finished!\n')
        generation = generation + 1
