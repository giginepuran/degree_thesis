from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import shutil
import os


def create_folder_to_id(drive: GoogleDrive, parent_id: str, folder_name: str):
    file_metadata = {
        'title': folder_name,
        'parents': [{'id': parent_id}],
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = drive.CreateFile(file_metadata)
    folder.Upload()
    return folder


def put_file_to_id(drive: GoogleDrive, parent_id: str, drive_file_id: str, local_file: str,
                   change_name=False, put_name="file_name"):
    if not os.path.exists(local_file):
        return
    file_metadata = {
        'parents': [{'id': parent_id}],
        'id': drive_file_id
    }
    file = drive.CreateFile(file_metadata)
    file.SetContentFile(local_file)
    original_filename = local_file[local_file.rfind('/')+1:]
    file['title'] = put_name if change_name else original_filename
    file.Upload()
    return file


# Compare to put_entire_dir_to_id, this function only put files,
# and won't create any folder
def put_all_files_to_id(drive: GoogleDrive, parent_id: str, local_dir: str, layer=0):
    if not os.path.isdir(local_dir):
        return
    file_list = os.listdir(local_dir)
    for file in file_list:
        if not os.path.isdir(f'{local_dir}/{file}'):
            put_file_to_id(drive, parent_id, f'{local_dir}/{file}')
        elif layer > 0:
            put_all_files_to_id(drive, parent_id, f'{local_dir}/{file}', layer-1)


def put_entire_dir_to_id(drive: GoogleDrive, parent_id: str, local_dir: str,
                         change_name=False, put_folder_name="folder_name"):
    if not os.path.isdir(local_dir):
        return
    # create an empty folder on drive, it will be save into dir_on_drive
    original_folder_name = local_dir[local_dir.rfind('/') + 1:]
    dir_on_drive = create_folder_to_id(drive, parent_id,
                                       put_folder_name if change_name else original_folder_name)
    # check all things under the local_dir
    file_list = os.listdir(local_dir)
    for file in file_list:
        # if it is a folder, doing recursion to put this folder entirely, without changing its name
        if os.path.isdir(f'{local_dir}/{file}'):
            put_entire_dir_to_id(drive, dir_on_drive['id'], f'{local_dir}/{file}')
        # if it is a file, upload it without changing its name
        else:
            put_file_to_id(drive, dir_on_drive['id'], f'{local_dir}/{file}')
    return dir_on_drive


def update_file(drive, parent_id, file_info, local_file):
    if not os.path.exists(local_file):
        return False
    put_file_to_id(drive, parent_id, file_info['id'], local_file)
    return True

