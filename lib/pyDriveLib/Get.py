from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import shutil
import os


def get_file_by_list(file_list: list, dst="", move=False):
    for file in file_list:
        file.GetContentFile(file['title'])
        if move and os.path.isdir(dst):
            filename = rename_if_file_exists(dst, file['title'])
            os.rename(file['title'], filename)
            shutil.move(filename, dst)


def get_drive_file_by_subtitle(drive: GoogleDrive, parent_id: str, subtitle: str, all_folder=False):
    file_list = drive.ListFile({'q': f"'{parent_id}' in parents and trashed=false"}).GetList()
    result = []
    for file in file_list:
        if subtitle in file['title']:
            result.append(file)
        elif all_folder and file['mimeType'] == 'application/vnd.google-apps.folder':
            result = result + get_drive_file_by_subtitle(drive, file['id'], subtitle, all_folder=True)
    return result


def rename_if_file_exists(path: str, filename: str):
    new_filename = filename
    count = 1
    while os.path.exists(f'{path}/{new_filename}'):
        sep_point = filename.rfind('.')
        new_filename = filename[:sep_point] + f'({count})' + filename[sep_point:]
        count = count+1
    return new_filename


def download_drive_file(file, dst="", move=False):
    file.GetContentFile(file['title'])
    if move and os.path.isdir(dst):
        shutil.move('./mode.txt', f"{dst}/{file['title']}")


