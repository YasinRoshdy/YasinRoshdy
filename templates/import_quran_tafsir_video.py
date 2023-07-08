import json
from operator import contains
import os
from pathlib import Path
from typing import Set

from base.management.commands.help import check_file_and_delete, mwasa_data_import
from base.management.commands.import_filer import AUDIOS, VIDEOS, get_path_audio, get_path_video, import_file

from base.models import Ayat, AyatTafsirVideo, BookInAlSaheh, ChapterInAlSaheh, Hadith, Sura, TafsirHadithInAlSaheh
from django.core.management.base import BaseCommand
from mwasa2.settings import BASE_DIR
from filer.models.filemodels import File as FilerFile, Folder as FilerFoldor

{
    "Id": "30",
    "FileName": "Quranv00029",
    "AyaFrom": "58",
    "SuraFrom": "سورة البقرة",
    "SuraFromId": "2",
    "AyaTo": "59",
    "SuraTo": "سورة البقرة",
    "SuraToId": "2",
    "YouTubeVideoID": "ljAntgffUHw",
}

{
    "Id": "134",
    "FileName": "Quranv00130",
    "AyaFrom": "1",
    "SuraFrom": "سورة آل عمران",
    "SuraFromId": "3",
    "AyaTo": "6",
    "SuraTo": "سورة آل عمران",
    "SuraToId": "3",
    "YouTubeVideoID": "10CFNmYJq6E",
},

TAFSEER_ALQURAN = "tafseer alquran"


def get_path_tafsir_video():
    Quran = "Quran"
    return get_path_video().joinpath(Quran).joinpath(Quran)


def tafseer_video():
    path = mwasa_data_import().joinpath("tafsire").joinpath("m_tafseer_video.json")
    ext = ".flv"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
        data = data[2]["data"]
        suras = Sura.objects.all()
        res = []
        found = 0
        not_found = 0
        for _ in data:

            sura = suras.filter(number=_["SuraToId"]).first()
            aya_start = Ayat.objects.filter(count=_["AyaFrom"]).first()
            aya_end = Ayat.objects.filter(count=_["AyaTo"]).first()
            file_name = f'{_["FileName"]}{ext}'
            oldf_path = get_path_tafsir_video().joinpath(file_name)
            if not _["FileName"]:
                continue

            TAFSEER_ALQURAN_File = FilerFile.objects.filter(file__icontains=_["FileName"]).first()
            if os.path.exists(oldf_path):
                found = found + 1
                # print(f"file exixt at {oldf_path} ")
                file = import_file(oldf_path, [VIDEOS, TAFSEER_ALQURAN])
                check_file_and_delete(oldf_path, file.path)

            elif TAFSEER_ALQURAN_File:
                found = found + 1
                # print(f"file TAFSEER_ALQURAN_File {TAFSEER_ALQURAN_File} ")
                file = import_file(TAFSEER_ALQURAN_File.path, [VIDEOS, TAFSEER_ALQURAN])
                check_file_and_delete(TAFSEER_ALQURAN_File.path, file.path)
                TAFSEER_ALQURAN_File.delete()

            else:
                print(f"continue file TAFSEER_ALQURAN not found_File {_['FileName']} ")
                not_found = not_found + 1

            res.append(
                AyatTafsirVideo(
                    sura=sura,
                    aya_start=aya_start,
                    aya_end=aya_end,
                    video_url=_["YouTubeVideoID"],
                    video_tafsir=file,
                )
            )
        AyatTafsirVideo.objects.bulk_create(res, ignore_conflicts=True)
        print("found", found)
        print("not_found", not_found)


class Command(BaseCommand):
    def handle(self, **options):
        tafseer_video()
