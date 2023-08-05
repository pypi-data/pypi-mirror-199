import json
import os
from pathlib import Path
import shutil
from dataclasses import fields

from .input_util import collect_input

class FileManager:
    @staticmethod
    def save_obj_to_file(file_path : str, d):
        with open(file_path,'wt',encoding='utf-8') as f:
            f.write(json.dumps(d))

    @staticmethod
    def read_file_as_single_line(file_path : str):
        with open(file_path,'rt',encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def read_file_as_multiple_lines(file_path : str):
        with open(file_path,'rt',encoding='utf-8') as f:
            return f.readlines()

    @staticmethod
    def get_obj_from_file(file_path : str):
        s=FileManager.read_file_as_single_line(file_path) #f.read()
        if s=='':
            return {}
        return json.loads(s)

    @staticmethod
    def get_objs_from_file(file_path : str):
        lines=FileManager.read_file_as_multiple_lines(file_path)
        return [json.loads(line) for line in lines]

    @staticmethod
    def save_str_to_file(file_path : str, s):
        with open(file_path,'wt',encoding='utf-8') as f:
            return f.write(s)

    @staticmethod
    def get_str_from_file(file_path : str):
        with open(file_path,'rt',encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def delete_all_files_in_folder(folder_path):
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        FileManager.ensure_folder_exists(folder_path)

    @staticmethod
    def ensure_folder_exists(folder_path):
        Path(folder_path).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def ensure_file_exists(file_path):
        if not os.path.exists(file_path):
            FileManager.save_str_to_file(file_path,'')

    @staticmethod
    def collect_and_save_input_for_undefined_fields(file_path : str, cls, is_valid_fxn=None):
        map = FileManager.get_obj_from_file(file_path)
        for field in fields(cls):
            if field.name not in map:
                new_val=collect_input(field, is_valid_fxn)
                map[field.name]=new_val
        FileManager.save_obj_to_file(file_path,map)
        return map

    @staticmethod
    def collect_and_save_input(file_path : str):
        map = FileManager.get_obj_from_file(file_path)
        new_map={}
        for key,dflt_val in map.items():
            new_val=input(f'{key} (default={dflt_val}): ')
            if new_val=='':
                new_val=dflt_val
            new_map[key]=new_val
        FileManager.save_obj_to_file(file_path,new_map)
        return new_map

    @staticmethod
    def get_row_count_in_file(file_path : str) -> int:
        with open(file_path,'rt',encoding='utf-8') as f:
            return len(f.readlines())