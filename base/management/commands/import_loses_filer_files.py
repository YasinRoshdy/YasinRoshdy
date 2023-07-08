import json
from base.management.commands.help import check_file_and_delete, mwasa_data_import
from base.management.commands.import_filer import AUDIOS, VIDEOS, import_file
from base.management.commands.import_other_science import RAMADANIAT, get_ramadaniat_video_Path

from base.models import Hadith
from django.core.management.base import BaseCommand
from mwasa2.settings import BASE_DIR
import filecmp
import os
from filer.models.filemodels import File as FilerFile, Folder as FilerFoldor


def filer_dir():
    return BASE_DIR.joinpath("media")


def check_file_and_not_delete(files_paths, files_names):
    if not (len(files_paths) > 1 and len(files_names) > 1):
        return
    file_lista = []

    for file_path, file_name in zip(files_paths, files_names):
        file_lista.append(filer_dir().joinpath(file_path).joinpath(file_name))

    # file_size = []
    # for file in file_lista:
    #     size = os.path.getsize(filer_dir().joinpath(file_path).joinpath(file_name))
    #     file_size.append(size)

    # print(f"file size {size}", sep=",")

    # os.remove()

    # if oldf_size == newf_size and filecmp.cmp(old, new):
    #     print("true file old {old} == {new}")
    # her to remove old file
    # cmp = []
    for file in file_lista[1:]:
        # check_file_and_delete(file_lista[0], file)
        pass
    # print(cmp)


class Command(BaseCommand):
    def handle(self, **options):
        filer_files = FilerFile.objects.all()
        with open(mwasa_data_import().joinpath("filenames.txt"), encoding="utf-8") as names:
            lines = names.readlines()
            file_names = []
            file_paths = []
            # {"file": "file_name", "file_path": "file_path"}
            index = 0
            for line in lines:
                if "." in line and "./" not in line:
                    file_names.append(line.strip())
                    file_paths.append(lines[index - 1].strip()[2:-1])
                index += 1

            # for name, path in zip(file_names, file_paths):
            #     print("name,path", name, path)
            for file_name, file_path in zip(file_names, file_paths):

                filer_file2 = filer_files.filter(file__contains=file_name).all()
                MAIN_DIR = AUDIOS if "mp3" in file_name else VIDEOS
                if not filer_file2:
                    oldf_path = filer_dir().joinpath(file_path).joinpath(file_name)
                    file = import_file(oldf_path, [MAIN_DIR, RAMADANIAT])
                    check_file_and_delete(oldf_path, file.path)
                    print("file_name ,file_path", file_name, file_path)
            file_names_tmp = file_names.copy()
            file_paths_tmp = file_paths.copy()
            unqie_vals = []
            for name in file_names:
                if name not in unqie_vals:
                    unqie_vals.append(name)

            for el in unqie_vals:
                count = file_names_tmp.count(el)
                names_tmp = []
                paths_tmp = []
                for i in range(count):

                    idx = file_names_tmp.index(el)
                    names_tmp.append(file_names[idx])
                    paths_tmp.append(file_paths[idx])

                check_file_and_not_delete(paths_tmp, names_tmp)
