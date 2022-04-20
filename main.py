from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from lib.pyDriveLib import Get
from lib.pyDriveLib import Put
import lib.MyLumerical.LumAPI
from lib.CommWithTaiwania import Taiwania
from lib.CommWithTaiwania import BuildHost
from lib.CommWithTaiwania import BuildHost_interpolation
from lib.CommWithTaiwania import Transfer

# this is a template main, use local_main.py to run

"""
build host local main template
"""
drive = Transfer.refresh_drive_by_gauth()
transfer_folder_id = '1E057cpokP4uldG6ZdoMLrk6p4JTEwmJ9'
# this must be a full path
local_transfer_folder = 'E:/degree_thesis/local/transfer'
saving_path = 'E:/degree_thesis/local/saving_path'
floor = [130, 180, 450, 0, 0, 0, -500]
ceiling = [230, 380, 650, 150, 150, 7, 1500]
dimension = 7
population = 10
max_generation = 50
BuildHost.build_work(population, max_generation, drive, transfer_folder_id,
                     local_transfer_folder, dimension, floor, ceiling, saving_path,
                     'E:/degree_thesis/script/lsf/pattern2/uniform.lsf',
                     lib.MyLumerical.LumAPI.get_transmission_wg2_fom)

"""
build host local main interpolation template
"""
drive = Transfer.refresh_drive_by_gauth()
transfer_folder_id = '1E057cpokP4uldG6ZdoMLrk6p4JTEwmJ9'
# this must be a full path
local_transfer_folder = 'E:/degree_thesis/local/transfer'
saving_path = 'E:/degree_thesis/local/saving_path'
floor = [-50, -50, -50, -50, -50,
         -50, -50, -50, -50, -50,
         0, 0, 0, 0, 0,
         -500, -500, -500, -500, -500]
ceiling = [150, 150, 150, 150, 150,
           150, 150, 150, 150, 150,
           5, 5, 5, 5, 5,
           1500, 1500, 1500, 1500, 1500]
parameter_num = 4
dimension = parameter_num * 5
population = 10
max_generation = 50
BuildHost_interpolation.build_work(population, max_generation, drive, transfer_folder_id,
                                   local_transfer_folder, dimension, parameter_num, floor, ceiling, saving_path,
                                   'E:/degree_thesis/script/lsf/pattern3/apodize.lsf',
                                   lib.MyLumerical.LumAPI.get_transmission_wg2_fom)
# opinion fom function below
# lib.MyLumerical.LumAPI.get_mode_mismatch_fom

"""
taiwania local main template
"""
drive = Transfer.refresh_drive_by_gauth()
transfer_folder_id = '1E057cpokP4uldG6ZdoMLrk6p4JTEwmJ9'
local_transfer_folder = '/home/u6097335/degree_thesis/local/transfer'
max_generation = 50
population = 10
Taiwania.taiwania_work(population, max_generation, drive, transfer_folder_id, local_transfer_folder)