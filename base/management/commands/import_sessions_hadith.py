import json
import os
from pathlib import Path
from typing import Set

from isort import file
from base.management.commands.help import check_file_and_delete, mwasa_content, mwasa_data_import
from base.management.commands.import_filer import AUDIOS, VIDEOS, get_path_audio, get_path_video, import_file

from base.models import (
    MEDIA_TYPE,
    SESSIONS_TYPE,
    Ayat,
    BookInAlSaheh,
    ChapterInAlSaheh,
    Fatwa,
    Hadith,
    OtherScience,
    OtherScienceSubject,
    Sessions,
    TafsirHadithInAlSaheh,
)
from django.core.management.base import BaseCommand
from mwasa2.settings import BASE_DIR
from django.db import models

# from filer.management.commands import generate_thumbnails
from filer.models.filemodels import File, Folder
from filer.models.filemodels import FileManager
from filer.management.commands.import_files import FileImporter

SESSIONS = "magales"

DIR_NAME = "شرح البخارى والاسئلة MP4 مجالس"


def import_sessions_hadith_path():
    return mwasa_content().joinpath(SESSIONS).joinpath(DIR_NAME)


_type = SESSIONS_TYPE[1][0]  # quran

exixt = 0
not_exixt = 0


def import_sessions_hadith():

    base_path = import_sessions_hadith_path()
    print("base_path", base_path)
    lista_subjects = os.listdir(base_path)
    sessions = []
    file_not_exixt = 0
    file_exixt = 0
    all = 0
    for book in lista_subjects:
        # print("sura", sura)
        # print(base_path.joinpath(sura))
        book_dirs_names = os.listdir(base_path.joinpath(book))

        for dir_name in book_dirs_names:
            files_in_dir = os.listdir(base_path.joinpath(book).joinpath(dir_name))
            for file_name in files_in_dir:
                # this may be file or dir

                file_path = base_path.joinpath(book).joinpath(dir_name).joinpath(file_name)
                if os.path.isdir(file_path):
                    lista_in_sub_dir = os.listdir(file_path)
                    for item_in_sub_dir in lista_in_sub_dir:
                        item_in_sub_dir_path = base_path.joinpath(book).joinpath(dir_name).joinpath(file_name).joinpath(item_in_sub_dir)

                        if os.path.isdir(item_in_sub_dir_path):
                            lista_in_sub_sub_dir = os.listdir(item_in_sub_dir_path)
                            for item_in_sub_sub_dir in lista_in_sub_sub_dir:
                                item_in_sub_sub_dir_path = (
                                    base_path.joinpath(book)
                                    .joinpath(dir_name)
                                    .joinpath(file_name)
                                    .joinpath(item_in_sub_dir)
                                    .joinpath(item_in_sub_sub_dir)
                                )
                                import_item(
                                    item_in_sub_sub_dir_path,
                                    item_in_sub_sub_dir,
                                    [VIDEOS, SESSIONS, DIR_NAME, dir_name, file_name, item_in_sub_dir, item_in_sub_sub_dir],
                                )

                        else:
                            import_item(
                                item_in_sub_dir_path, item_in_sub_dir, [VIDEOS, SESSIONS, DIR_NAME, dir_name, file_name, item_in_sub_dir]
                            )

                else:
                    import_item(file_path, file_name, [VIDEOS, SESSIONS, DIR_NAME, dir_name, file_name])
                # all = all + 1

            # sessions.append(Sessions(file=file, title=file_name, type=type).save())

    # Sessions.objects.bulk_create(sessions)
    print("exixt", exixt)
    print("nott exixt", not_exixt)


def print_item(file_path, file_name, dirs_list):
    global exixt
    global not_exixt
    if os.path.exists(file_path):
        print("exixt", file_path, "dirs lista ", dirs_list)
        exixt = exixt + 1
    else:
        print("not exixt", file_path, "dirs lista ", dirs_list)
        not_exixt = not_exixt + 1


def import_item(file_path, file_name, dirs_list):
    # if file_name.count(".") == 2 or "DS_Store" in file_name:
    #     file_not_exixt = file_not_exixt + 1

    #     print("file_name", file_name)
    #     print("ignore:", file_path)
    #     print("size", os.path.getsize(file_path))
    # el
    global exixt
    global not_exixt
    global _type
    if os.path.isfile(file_path):
        print("is file , ", file_path)
        exixt = exixt + 1

        file = import_file(file_path, dirs_list)
        check_file_and_delete(file_path, file.path)
        Sessions(file=file, title=file_name, type=_type).save()
        print("added")
    else:
        not_exixt = not_exixt + 1


# def item_import():
#     file = import_file()
#     return


# def import_sessions_quran():

#     with open(mwasa_data_import().joinpath("").joinpath("filenames.txt")) as names:
#         lines = names.readline()
#         for line in lines:
#             pass


class Command(BaseCommand):
    def handle(self, **options):

        import_sessions_hadith()
