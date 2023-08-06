import hashlib
import os
import pathlib
from dataclasses import dataclass


@dataclass
class FileInfo():
    filename:str
    md5:str


def rename_file_to_hash(file_path:str) -> FileInfo:
    with open(file_path, 'rb') as file_to_check:
        data = file_to_check.read()    
        md5_returned = hashlib.md5(data).hexdigest()
        path = os.path.dirname(file_path)
        extension = pathlib.Path(file_path).suffix
        filename = f'{md5_returned}{extension}'
        os.rename(file_path, f"{path}/{filename}")
    return FileInfo(filename=filename, md5=md5_returned)
