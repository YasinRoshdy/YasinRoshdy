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

DIR_NAME = "تفسير القرآن الكريم  MP4 مجالس"


def import_sessions_quran_path():
    return mwasa_content().joinpath(SESSIONS).joinpath(DIR_NAME)


def import_sessions_quran():

    base_path = import_sessions_quran_path()
    print("base_path", base_path)
    lista_subjects = os.listdir(base_path)
    type = SESSIONS_TYPE[0][0]  # quran
    sessions = []
    file_not_exixt = 0
    file_exixt = 0
    all = 0
    for sura in lista_subjects:
        # print("sura", sura)
        # print(base_path.joinpath(sura))
        sura_files_names = os.listdir(base_path.joinpath(sura))

        for file_name in sura_files_names:
            all = all + 1
            file_path = base_path.joinpath(sura).joinpath(file_name)
            if file_name.count(".") == 2 or "DS_Store" in file_name:
                file_not_exixt = file_not_exixt + 1

                print("file_name", file_name)
                print("ignore:", file_path)
                print("size", os.path.getsize(file_path))
            elif os.path.isfile(base_path.joinpath(sura).joinpath(file_name)):
                print("added")
                file_exixt = file_exixt + 1

                file = import_file(file_path, [VIDEOS, SESSIONS, type, sura])
                check_file_and_delete(file_path, file.path)
                Sessions(file=file, title=file_name, type=type).save()

            # sessions.append(Sessions(file=file, title=file_name, type=type).save())

    # Sessions.objects.bulk_create(sessions)

    print("file_not_exixt", file_not_exixt)
    print("file_exixt", file_exixt)
    print("all", all)


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

        import_sessions_quran()
