import shutil
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from lib.pyDriveLib import Build
from lib.pyDriveLib import Get
from lib.pyDriveLib import Put
from lib.CommWithTaiwania import Transfer
import os
import time
import lumapi
from lib.PSO import swarm
from lib.PSO import particle
from lib.MyLumerical import PSO_Flow
from lib.CommWithTaiwania import BuildHost


def initialize_drive_transfer_folder(drive: GoogleDrive, transfer_folder_id: str, population: int):
    file_list = drive.ListFile({'q': f"'{transfer_folder_id}' in parents and trashed=false"}).GetList()
    for file in file_list:
        drive.CreateFile({'id': file['id']}).Delete()
    for i in range(1, population+1):
        Put.create_file_to_id(drive, transfer_folder_id, './local/ind_template.fsp',
                              change_name=True, put_name=f'ind{i}.fsp')
    Put.create_file_to_id(drive, transfer_folder_id, './local/mode_template.txt',
                          change_name=True, put_name='mode.txt')


gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

transfer_folder_id = '1E057cpokP4uldG6ZdoMLrk6p4JTEwmJ9'
population = 20

print('Initializing transfer folder on google drive ...')
initialize_drive_transfer_folder(drive, transfer_folder_id, population)
