from io import FileIO
import json
import os
from pathlib import Path
from base.management.commands.help import check_file_and_delete, mwasa_data_import
from base.management.commands.import_filer import AUDIOS, VIDEOS, get_path_audio, get_path_video, import_file
from base.models import Ayat, AyatTafsirAudio, AyatTafsirVideo, AyatTelawa, Book, BookSeach, Sura
from django.core.management.base import BaseCommand

from filer.models.filemodels import File as FilerFile, Folder as FilerFoldor

{
    "Id": "10",
    "FileName": "002_058_061",
    "AyaTo": "61",
    "SuraTo": "البقرة",
    "SuraToId": "2",
    "AyaFrom": "58",
    "SuraFrom": "البقرة",
    "SuraFromId": "2",
}
{
    "Id": "51",
    "FileName": "003_001_009",
    "AyaTo": "9",
    "SuraTo": "آل عمران",
    "SuraToId": "3",
    "AyaFrom": "1",
    "SuraFrom": "آل عمران",
    "SuraFromId": "3",
},

TAFSEER_ALQURAN_AUDIO = "tafseer alquran"


def get_path_tafsir_audio():
    return get_path_audio().joinpath(TAFSEER_ALQURAN_AUDIO)


def tafseer_audio():
    found = 0
    file_ext = ".mp3"
    path = mwasa_data_import().joinpath("tafsire").joinpath("m_tafseer_audio.json")

    AUDIOSFoldor = FilerFoldor.objects.filter(name__icontains=AUDIOS).first()
    print(AUDIOSFoldor)
    TAFSEER_ALQURAN_AUDIO_Foldor = FilerFoldor.objects.filter(name__icontains=TAFSEER_ALQURAN_AUDIO, parent=AUDIOSFoldor).first()
    print(TAFSEER_ALQURAN_AUDIO_Foldor)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
        data = data[2]["data"]
        suras = Sura.objects.all()
        res = []
        for _ in data:

            sura = suras.filter(number=_["SuraToId"]).first()
            aya_start = Ayat.objects.filter(count=_["AyaFrom"]).first()
            aya_end = Ayat.objects.filter(count=_["AyaTo"]).first()
            filesname = _["FileName"]

            # filesnames = _["FileName"].split(" _ ")
            # for filename in filesnames:
            TAFSEER_ALQURAN_File = FilerFile.objects.filter(file__icontains=_["FileName"], folder=TAFSEER_ALQURAN_AUDIO_Foldor).first()

            if TAFSEER_ALQURAN_File:

                print("TAFSEER_ALQURAN_File", TAFSEER_ALQURAN_File)
                found = found + 1
                file = TAFSEER_ALQURAN_File
            elif os.path.exists(get_path_tafsir_audio().joinpath(f"{filesname}{file_ext}")):
                file = import_file(get_path_tafsir_audio().joinpath(f"{filesname}{file_ext}"), [AUDIOS, TAFSEER_ALQURAN_AUDIO])
            else:
                continue

            res.append(AyatTafsirAudio(sura=sura, aya_start=aya_start, aya_end=aya_end, sound_tafsir=file))
        AyatTafsirAudio.objects.bulk_create(res)
        print(found)


{
    "id": "7",
    "FileName": "telwa007",
    "ToAya": "سورة البقرة آية 202",
    "FromAya": "سورة البقرة آية 177",
}

TELAWA = "Telawa"


def get_path_telawa_audio():
    return get_path_audio().joinpath(TELAWA)


def telawa():

    AUDIOSFoldor = FilerFoldor.objects.filter(name__icontains=AUDIOS).first()
    print(AUDIOSFoldor)
    TAFSEER_ALQURAN_AUDIO_Foldor = FilerFoldor.objects.filter(name__icontains=TELAWA, parent=AUDIOSFoldor).first()
    print(TAFSEER_ALQURAN_AUDIO_Foldor)
    file_ext = ".mp3"
    path = mwasa_data_import().joinpath("tafsire").joinpath("audio_telawa.json")
    exixt = 0
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
        data = data[2]["data"]

        res = []
        print(len(data))
        length = 0
        for _ in data:
            if int(_["id"]) >= 172:
                sura = None
                aya_start = None
                aya_end = None
            else:
                sura_name = " ".join(_["ToAya"].split(" ")[1:-2]).strip()
                sura = Sura.objects.filter(name=sura_name).first()

                aya_start = Ayat.objects.filter(count=_["FromAya"].split(" ")[-1]).first()
                aya_end = Ayat.objects.filter(count=_["ToAya"].split(" ")[-1]).first()

            TAFSEER_ALQURAN_File = FilerFile.objects.filter(file__icontains=_["FileName"], folder=TAFSEER_ALQURAN_AUDIO_Foldor).first()

            old_file_path = get_path_telawa_audio().joinpath(f'{_["FileName"]}{ file_ext}')
            if TAFSEER_ALQURAN_File:
                file = import_file(old_file_path, [AUDIOS, TELAWA])
                exixt += 1

            elif os.path.exists(old_file_path):
                file = import_file(old_file_path, [AUDIOS, TELAWA])
                # exixt += 1
            else:
                print(old_file_path)
                continue
                # check_file_and_delete(old_file_path,file.path)

            res.append(
                AyatTelawa(
                    sura=sura,
                    aya_start=aya_start,
                    aya_end=aya_end,
                    telawa=file,
                )
            )
        AyatTelawa.objects.bulk_create(res)

        print("exixt , ", exixt)


class Command(BaseCommand):
    def handle(self, **options):
        # tafseer_audio()
        # tafseer_video()
        telawa()
