from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from lib.pyDriveLib import Get
from lib.pyDriveLib import Put
import os
import time


def keep_check_mode(mode_file_info, local_transfer_folder: str, mode_msg: str, period=30):
    drive = refresh_drive_by_gauth()
    count = 0
    while True:
        if count > 900:
            drive = refresh_drive_by_gauth()
            count = count - 900
        Get.download_drive_file(drive, mode_file_info, dst=local_transfer_folder, move=True)
        mode = open(f'{local_transfer_folder}/mode.txt', 'r').read()
        if mode_msg in mode:
            break
        else:
            count = count + period
            time.sleep(period)


def update_fsps(drive: GoogleDrive, parent_id: str, file_info_list: list, local_transfer_folder: str, population: int):
    suc_num = 0
    for file_info in file_info_list:
        title = file_info['title']
        if '.fsp' not in title:
            continue
        if Put.update_file(drive, parent_id, file_info, f'{local_transfer_folder}/{title}'):
            suc_num = suc_num + 1
        if suc_num % 31 == 30:
            drive = refresh_drive_by_gauth()
    if suc_num != population:
        print(f'number of fsp files uploaded is wrong\nActually number : {suc_num}\nExpected : {population}')
        return False
    return True


def change_mode_then_upload(drive: GoogleDrive, parent_id: str, mode_file_info,
                            local_transfer_folder: str, mode_msg: str):
    msg = os.popen(f'echo {mode_msg} > {local_transfer_folder}/mode.txt').read()
    Put.update_file(drive, parent_id, mode_file_info, f'{local_transfer_folder}/mode.txt')


def refresh_drive_by_gauth():
    gauth = GoogleAuth()
    scope = ["https://www.googleapis.com/auth/drive"]
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('E:/degree_thesis/local/u6097335.json', scope)
    return GoogleDrive(gauth)

