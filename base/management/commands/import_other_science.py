import json
import os
from pathlib import Path
from typing import Set

from isort import file
from base.management.commands.help import check_file_and_delete, mwasa_content, mwasa_data_import
from base.management.commands.import_filer import AUDIOS, VIDEOS, get_path_audio, get_path_video, import_file
from filer.models.filemodels import File as FilerFile, Folder as FilerFoldor

from base.models import (
    MEDIA_TYPE,
    Ayat,
    BookInAlSaheh,
    ChapterInAlSaheh,
    Fatwa,
    Hadith,
    OtherScience,
    OtherScienceSubject,
    TafsirHadithInAlSaheh,
)
from django.core.management.base import BaseCommand
from mwasa2.settings import BASE_DIR
from django.db import models

# from filer.management.commands import generate_thumbnails

from filer.management.commands.import_files import FileImporter

# from filer.fields.folder import Folder
{
    "id": "1072",
    "Catg_id": "10",
    "catg": "في رحاب المصطفى المختار صلى الله عليه وسلم",
    "title": "المسلمون في المدينة 2",
    "filename": "FerehabS027",
    "folder": "Fe Rehab almostafa",
    "YouTubeVideoID": "8KyYT88nwd4",
},

RAMADANIAT = "Ramadniat"
RAMADANIAT_VIDEO = "Ramadaniat"


def get_ramadaniat_audio_Path():
    return get_path_audio().joinpath(RAMADANIAT)


def get_ramadaniat_video_Path():
    return get_path_video().joinpath(RAMADANIAT_VIDEO)


{
    "id": "1",
    "Catg_id": "1",
    "catg": "هو الله",
    "filename": "Hoa01",
    "title": "(الرحمن - الرحيم - الملك - القدوس - السلام – المؤمن)",
    "folder": "Hoa Allah",
},


# def import_ramadaniat_audio():
#     ext = ".mp3"
#     base_path = get_ramadaniat_audio_Path()
#     lista_subjects = os.listdir(base_path)

#     subjects = []
#     others = []
#     for lista_subject in lista_subjects:

#         lista_subject = lista_subject.strip()
#         print("lista_subject", lista_subject)
#         subject = OtherScienceSubject.objects.filter(subjects=lista_subject, file_type=MEDIA_TYPE[0][0]).first()
#         if not subject:
#             subject = OtherScienceSubject(file_type=MEDIA_TYPE[1][0], subjects=lista_subject)
#             # subjects.append(subject)
#             subject.save()

#         lista_subjects_items = os.listdir(base_path.joinpath(lista_subject))

#         for item in lista_subjects_items:
#             print("item", item)
#             file = file = import_file(f"{base_path.joinpath(lista_subject).joinpath( item)}", [AUDIOS, RAMADANIAT, f"{lista_subject}"])
#             others.append(OtherScience(title=item, file=file, subject=subject))

#     # OtherScienceSubject.objects.bulk_create(subjects)
#     OtherScience.objects.bulk_create(others)
{
    "id": "12",
    "Catg_id": "1",
    "catg": "هو الله",
    "filename": "Hoa12",
    "title": "الإلحاد",
    "folder": "Hoa Allah",
}


def import_ramadaniat_audio():
    with open(mwasa_data_import().joinpath(RAMADANIAT).joinpath("audio.json"), encoding="utf-8") as f:
        data = json.load(f)
        data = data[2]["data"]

        ext = ".mp3"
        base_path = get_ramadaniat_audio_Path()

        others = []
        for _ in data:

            print("_", _, sep=",")
            catg = _["catg"].strip()
            subject = OtherScienceSubject.objects.filter(subjects=catg, file_type=MEDIA_TYPE[1][0]).first()
            if not subject:
                subject = OtherScienceSubject(file_type=MEDIA_TYPE[1][0], subjects=catg)
                # subjects.append(subject)
                subject.save()
            file_n = f'{_["filename"]}{ext}'
            oldf_path = base_path.joinpath(_["folder"]).joinpath(file_n)
            # file_dir_filer = FilerFoldor.objects.filter(name=_["folder"]).first()
            TAFSEER_ALQURAN_File = FilerFile.objects.filter(file__icontains=file_n).first()

            if os.path.exists(oldf_path):
                print("os.path is exist")
                file = import_file(oldf_path, [AUDIOS, RAMADANIAT, _["folder"]])
                check_file_and_delete(oldf_path, file.path)
            elif TAFSEER_ALQURAN_File:

                print("TAFSEER_ALQURAN_File is exist")

                file = import_file(TAFSEER_ALQURAN_File.path, [AUDIOS, RAMADANIAT, _["folder"]])
                check_file_and_delete(TAFSEER_ALQURAN_File.path, file.path)
                TAFSEER_ALQURAN_File.delete()
            else:
                print("continue ")
                continue

            others.append(OtherScience(title=_["title"][0:254], file=file, subject=subject))

        OtherScience.objects.bulk_create(others)


{
    "id": "6",
    "Catg_id": "1",
    "catg": "الأحاديث القدسية - رمضان 1984",
    "title": "نبأ عظيم 2",
    "filename": "A7adthS006",
    "folder": "Ala7adeth AlKodusia",
    "YouTubeVideoID": "MJKYXDagP-Y",
},
{
    "id": "1",
    "Catg_id": "1",
    "catg": "الأحاديث القدسية - رمضان 1984",
    "title": "المقدمة \/ القناعة بالكفايه 1",
    "filename": "A7adthS001",
    "folder": "Ala7adeth AlKodusia",
    "YouTubeVideoID": "LN3QphwoRaw",
},


def import_ramadaniat_video():
    with open(mwasa_data_import().joinpath(RAMADANIAT).joinpath("video.json"), encoding="utf-8") as f:
        data = json.load(f)
        data = data[2]["data"]

        ext = ".flv"
        base_path = get_ramadaniat_video_Path()

        others = []
        for _ in data:

            print("_", _)
            catg = _["catg"].strip()
            subject = OtherScienceSubject.objects.filter(subjects=catg, file_type=MEDIA_TYPE[0][0]).first()
            if not subject:
                subject = OtherScienceSubject(file_type=MEDIA_TYPE[0][0], subjects=catg)
                subject.save()
            file_n = f'{_["filename"]}{ext}'
            file_path = base_path.joinpath(_["folder"]).joinpath(file_n)
            # file_dir_filer = FilerFoldor.objects.filter(name=_["folder"]).first()
            TAFSEER_ALQURAN_File = FilerFile.objects.filter(file__icontains=file_n).first()
            if os.path.exists(file_path):
                print("os.path is exist")

                file = import_file(file_path, [VIDEOS, RAMADANIAT_VIDEO, _["folder"]])
                check_file_and_delete(file_path, file.path)
            elif TAFSEER_ALQURAN_File:
                print("TAFSEER_ALQURAN_File is exist")
                file = import_file(TAFSEER_ALQURAN_File.path, [VIDEOS, RAMADANIAT, _["folder"]])
                check_file_and_delete(TAFSEER_ALQURAN_File.path, file.path)
                TAFSEER_ALQURAN_File.delete()

            else:
                print("continue ")
                continue
            others.append(OtherScience(title=_["title"][0:254], file=file, subject=subject, video_url=_["YouTubeVideoID"]))

        OtherScience.objects.bulk_create(
            others,
            #  ignore_conflicts=True
        )


class Command(BaseCommand):
    def handle(self, **options):

        import_ramadaniat_audio()
        import_ramadaniat_video()
