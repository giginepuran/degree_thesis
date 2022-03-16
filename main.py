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
import os
import time


gauth = GoogleAuth()
scope = ["https://www.googleapis.com/auth/drive"]
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('./local/u6097335.json', scope)
drive = GoogleDrive(gauth)

transfer_folder_id = '1E057cpokP4uldG6ZdoMLrk6p4JTEwmJ9'
# this must be a full path
local_transfer_folder = 'C:/Users/clay0/workshop/coding/python/degree_thesis/local/transfer'
Taiwania.taiwania_work(3, 10, drive, transfer_folder_id, local_transfer_folder)
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