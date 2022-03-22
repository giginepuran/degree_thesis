# this is a template main, use local_main.py to run

# build host local main template
"""
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from lib.pyDriveLib import Get
from lib.pyDriveLib import Put
from lib.CommWithTaiwania import Taiwania
from lib.CommWithTaiwania import BuildHost
from lib.CommWithTaiwania import Transfer
import os
import time


drive = Transfer.refresh_drive_by_gauth()

transfer_folder_id = '1E057cpokP4uldG6ZdoMLrk6p4JTEwmJ9'
# this must be a full path
local_transfer_folder = 'E:/degree_thesis/local/transfer'
saving_path = 'E:/degree_thesis/local/saving_path'

floor = [100, 100, 100, 50, 10]
ceiling = [300, 300, 300, 200, 90]
dimension = 5
population = 5
max_generation = 50

BuildHost.build_work(population, max_generation, drive, transfer_folder_id,
                     local_transfer_folder, dimension, floor, ceiling, saving_path)
"""


# taiwania local main template
"""
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from lib.pyDriveLib import Build
from lib.pyDriveLib import Get
from lib.pyDriveLib import Put
from lib.CommWithTaiwania import Transfer
from lib.CommWithTaiwania import Taiwania
from google.oauth2 import service_account
import os
import time


drive = Transfer.refresh_drive_by_gauth()

transfer_folder_id = '1E057cpokP4uldG6ZdoMLrk6p4JTEwmJ9'
local_transfer_folder = '/home/u6097335/degree_thesis/local/transfer'

Taiwania.taiwania_work(5, 50, drive, transfer_folder_id, local_transfer_folder)
"""


# build host local main interpolation template
""" 
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from lib.pyDriveLib import Get
from lib.pyDriveLib import Put
from lib.CommWithTaiwania import Taiwania
from lib.CommWithTaiwania import BuildHost
from lib.CommWithTaiwania import BuildHost_interpolation
from lib.CommWithTaiwania import Transfer
import os
import time


drive = Transfer.refresh_drive_by_gauth()

transfer_folder_id = '1E057cpokP4uldG6ZdoMLrk6p4JTEwmJ9'
# this must be a full path
local_transfer_folder = 'E:/degree_thesis/local/transfer'
saving_path = 'E:/degree_thesis/local/saving_path'

floor = [100, 100, 100, 100, 100,
         100, 100, 100, 100, 100,
         100, 100, 100, 100, 100,
         50,  50,  50,  50,  50,
         10,  10,  10,  10,  10]
ceiling = [300, 300, 300, 300, 300,
           300, 300, 300, 300, 300,
           300, 300, 300, 300, 300,
           200, 200, 200, 200, 200,
           90,  90,  90,  90,  90]
dimension = 25
population = 25
max_generation = 100

BuildHost_interpolation.build_work(population, max_generation, drive, transfer_folder_id,
                                   local_transfer_folder, dimension, floor, ceiling, saving_path)
"""