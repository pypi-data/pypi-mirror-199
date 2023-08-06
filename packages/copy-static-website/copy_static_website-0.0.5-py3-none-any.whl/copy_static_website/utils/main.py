# Python built-in libraries
import os
from typing import Union
from ftplib import FTP

def create_dir_recursively(dir):
    if not os.path.exists(dir):
        head, tail = os.path.split(dir)
        if head != '':
            create_dir_recursively(head)
        os.mkdir(dir)

def ftp_check_if_path_exists(ftp: FTP, path: str) -> bool:
    head, tail = os.path.split(path)
    if head == '':
        head = '/'
    for name, facts in ftp.mlsd(head):
        # 'name' is the name of the file or directory being analyzed.
        # 'facts' is a dict containing properties of that object, like type,
        # size, date of modification, etc.
        if name == tail:
            return True
    return False

def remove_parent_folder_from_path(path: os.PathLike) -> Union[os.PathLike, None]:
    head, tail = os.path.split(path)
    path_parts = [tail]
    while head != '':
        head, tail = os.path.split(head)
        path_parts.append(tail)
    path_parts = path_parts[:-1] # remove the last item (the parent folder)
    path_parts.reverse()
    if len(path_parts) > 0:
        return os.path.join(*path_parts)
    else:
        return None

def join_path_parts_ignore_none(path_parts: list[Union[os.PathLike, None]]) -> os.PathLike:
    parts_to_join = []
    for part in path_parts:
        if part != None:
            parts_to_join.append(part)
    if len(parts_to_join) > 0:
        return os.path.join(*parts_to_join)
    else:
        return '/'