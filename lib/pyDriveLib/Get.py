from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from lib.CommWithTaiwania import Transfer
import shutil
import os


def get_file_info_by_subtitle(drive: GoogleDrive, parent_id: str, subtitle: str, all_folder=False):
    file_list = drive.ListFile({'q': f"'{parent_id}' in parents and trashed=false"}).GetList()
    result = []
    for file in file_list:
        if subtitle in file['title']:
            result.append({'id': file['id'], 'title': file['title']})
        elif all_folder and file['mimeType'] == 'application/vnd.google-apps.folder':
            result = result + get_file_info_by_subtitle(drive, file['id'], subtitle, all_folder=True)
    return result


def download_drive_file(drive: GoogleDrive, file_info, dst="", move=False):
    suc = False
    while not suc:
        try:
            file = drive.CreateFile({'id': file_info['id']})
            file.GetContentFile(file['title'])
            if move and os.path.isdir(dst):
                shutil.move(f"./{file['title']}", f"{dst}/{file['title']}")
            suc = True
        except:
            print(f"download {file_info['title']} failed.")
            drive = Transfer.refresh_drive_by_gauth()



