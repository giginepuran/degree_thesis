# this is a template main, use local_main.py to run

# build host local main template
"""
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from lib.pyDriveLib import Build
from lib.pyDriveLib import Get
from lib.pyDriveLib import Put
from lib.CommWithTaiwania import Taiwania
from lib.CommWithTaiwania import BuildHost
import os
import time


gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

transfer_folder_id = '1E057cpokP4uldG6ZdoMLrk6p4JTEwmJ9'
# this must be a full path
local_transfer_folder = 'E:/degree_thesis/local/transfer'
saving_path = 'E:/degree_thesis/local/saving_path'

floor = [100, 100, 100, 50, 10]
ceiling = [300, 300, 300, 200, 90]
dimension = 5

BuildHost.build_work(3, 10, drive, transfer_folder_id, local_transfer_folder, dimension, floor, ceiling, saving_path)
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
import os
import time


# uctAFSct2mT472L
gauth = GoogleAuth()
scope = ["https://www.googleapis.com/auth/drive"]
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('./local/u6097335.json', scope)
drive = GoogleDrive(gauth)

transfer_folder_id = '1E057cpokP4uldG6ZdoMLrk6p4JTEwmJ9'
local_transfer_folder = '/home/u6097335/degree_thesis/local/transfer'

Taiwania.taiwania_work(3, 10, drive, transfer_folder_id, local_transfer_folder)
"""