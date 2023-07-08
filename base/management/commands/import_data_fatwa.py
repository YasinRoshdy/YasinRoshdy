import json
import os
from pathlib import Path
from typing import Set

from isort import file
from base.management.commands.help import mwasa_content, mwasa_data_import
from base.management.commands.import_filer import AUDIOS, get_path_audio, import_file

from base.models import Ayat, BookInAlSaheh, ChapterInAlSaheh, Fatwa, Hadith, TafsirHadithInAlSaheh
from django.core.management.base import BaseCommand
from mwasa2.settings import BASE_DIR
from django.db import models

# from filer.management.commands import generate_thumbnails
from filer.models.filemodels import File, Folder
from filer.models.filemodels import FileManager
from filer.management.commands.import_files import FileImporter

# from filer.fields.folder import Folder

{
    "id": "1",
    "Catg_id": "20",
    "catg": "الفتاوى",
    "filename": "Fatwa01",
    "title": "حب الرسول صلي الله عليه و سلم",
    "folder": "Fatwa",
}
FATWA = "Fatwa"
RAMADANIAT = "Ramadniat"


def get_Fatwa_Path():
    # return mwasa_content().joinpath(AUDIOS).joinpath(RAMADANIAT).joinpath(FATWA)
    return get_path_audio().joinpath(RAMADANIAT).joinpath(FATWA)


class Command(BaseCommand):
    def handle(self, **options):
        ext = ".mp3"
        lista_fatwa = []
        # FilerFileField
        # Folder
        with open(mwasa_data_import().joinpath("fatwa.json"), encoding="utf-8") as f:

            # data = open(BASE_DIR.parent.joinpath("data-import").joinpath("fatwa.json"), encoding="utf-8")
            data = json.load(f)
            data = data[2]["data"]

            for _ in data:

                _file = import_file(get_Fatwa_Path().joinpath(f'{_["filename"]}{ext}'), [AUDIOS, RAMADANIAT, FATWA])

                lista_fatwa.append(Fatwa(title=_["title"], file=_file))

        Fatwa.objects.bulk_create(lista_fatwa)


# def get_dummy_dir():
#     return BASE_DIR.joinpath("base", "temp")


# def create_dumy_file(file_name, dir):
#     dir_path = BASE_DIR.joinpath("base", "temp", dir)
#     if not dir_path.is_dir():
#         dir = os.mkdir(dir_path)

#     path = BASE_DIR.joinpath(dir_path, file_name)
#     if not path.is_file():
#         file = open(path, "w")

#         file.close()
#     return path
