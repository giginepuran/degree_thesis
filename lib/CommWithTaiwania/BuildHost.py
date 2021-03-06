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


def build_work(is_local: bool, population: int, max_generation: int, drive: GoogleDrive,
               transfer_folder_id: str, local_transfer_folder: str,
               dimension: int, floor: list, ceiling: list, saving_path: str,
               build_lsf: str, fom_function, inherit_path: str):
    print('PSO settings:')
    print(f'local transfer folder : {local_transfer_folder}')
    print(f'          saving path : {saving_path}')
    print(f'       max generation : {max_generation}')
    print(f'           population : {population}')
    print(f'            dimension : {dimension}')
    print('-------------------------------------')

    print('initializing saving path ...')
    PSO_Flow.step1_initialize_saving_path(saving_path, max_generation, population)

    print('opening fdtd gui ...')
    fdtd = lumapi.FDTD(hide=False)

    print('Creating swarm ...')
    my_swarm = PSO_Flow.step2_create_swarm(dimension, population, floor, ceiling)
    if os.path.isdir(inherit_path):
        print('----- Inherit path is found. -----')
        my_swarm.particles[0].inherit(dimension, inherit_path)

    print(f'Getting ids of mode_file and fsp_list ...')
    mode_file_info = Get.get_file_info_by_subtitle(drive, transfer_folder_id, 'mode.txt', all_folder=False)[0]
    fsp_info_list = Get.get_file_info_by_subtitle(drive, transfer_folder_id, '.fsp', all_folder=False)
    if len(fsp_info_list) != population:
        print(f'number of fsp files is wrong\nActually number : {len(fsp_info_list)}\nExpected : {population}')
        return

    drive = Transfer.refresh_drive_by_gauth()
    Transfer.change_mode_then_upload(drive, transfer_folder_id, mode_file_info, local_transfer_folder, 'building_fsp')

    print('Build host start working ...\n')
    generation = 1
    while generation <= max_generation:
        print(f'Building with generation{generation}')
        print('-------------------------------------')

        print('Building fsp ...')
        PSO_Flow.step3_build_fsp_by_swarm(fdtd, my_swarm, build_lsf,
                                          local_transfer_folder, dimension, population)

        if is_local:
            print('FDTDing *.fsp in local ...')
            PSO_Flow.local_fdtd_fsp(local_transfer_folder, population, fdtd)
        else:
            print('Updating *.fsp to drive transfer folder ...')
            drive = Transfer.refresh_drive_by_gauth()
            if not Transfer.update_fsps(drive, transfer_folder_id, fsp_info_list, local_transfer_folder, population):
                return

            print('Updating mode.txt to drive transfer folder ...')
            drive = Transfer.refresh_drive_by_gauth()
            Transfer.change_mode_then_upload(drive, transfer_folder_id, mode_file_info, local_transfer_folder,
                                             'doing_fdtd')

            print('Checking mode.txt ...')
            Transfer.keep_check_mode(mode_file_info, local_transfer_folder, 'building_fsp', period=30)

            print('Downloading *.fsp ...')
            drive = Transfer.refresh_drive_by_gauth()
            for fsp_info in fsp_info_list:
                Get.download_drive_file(drive, fsp_info, dst=local_transfer_folder, move=True)

        print('Collecting data from *.fsp ...')
        fom = PSO_Flow.step4_get_fom_of_each_particle(fdtd, population, local_transfer_folder, fom_function)

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

        print('Removing excess fsp')
        PSO_Flow.step11_remove_some_fsp(saving_path, generation, population)

        print('Particles evolving ...')
        my_swarm.evolution()

        print(f'Saving data of generation {generation} finished!\n')
        generation = generation + 1
