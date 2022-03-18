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


gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

transfer_folder_id = '1E057cpokP4uldG6ZdoMLrk6p4JTEwmJ9'
population = 5

print('Initializing transfer folder on google drive ...')
BuildHost.initialize_drive_transfer_folder(drive, transfer_folder_id, population)
