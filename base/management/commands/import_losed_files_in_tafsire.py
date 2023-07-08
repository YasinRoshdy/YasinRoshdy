import json
from base.management.commands.help import check_file_and_delete, mwasa_data_import
from base.management.commands.import_filer import AUDIOS, VIDEOS, import_file
from base.management.commands.import_other_science import RAMADANIAT, get_ramadaniat_video_Path
from base.management.commands.import_quran_tafsir_video import TAFSEER_ALQURAN, get_path_tafsir_video
from base.management.commands.import_quran_tafsire_telawa import get_path_tafsir_audio

from base.models import Ayat, AyatTafsirAudio, AyatTafsirVideo, Hadith, Sura
from django.core.management.base import BaseCommand
from mwasa2.settings import BASE_DIR
import filecmp
import os
from filer.models.filemodels import File as FilerFile, Folder as FilerFoldor
from django.db.models import Q


def val_if_none(var, val):
    return var if var else val


{
    "Id": "1100",
    "FileName": "Quran92",
    "AyaFrom": "75",
    "SuraFrom": "سورة الواقعة",
    "SuraFromId": "56",
    "AyaTo": "96",
    "SuraTo": "سورة الواقعة",
    "SuraToId": "56",
    "YouTubeVideoID": "6YTw9WDtDgk",
},
{
    "Id": "718",
    "FileName": "Quranv00693",
    "AyaFrom": "51",
    "SuraFrom": "سورة السجدة",
    "SuraFromId": "32",
    "AyaTo": "52",
    "SuraTo": "سورة السجدة",
    "SuraToId": "32",
    "YouTubeVideoID": "J2UO-CUAHgQ",
},


def import_losed_data_tafsir_fix_video():
    AyatTafsirVideo.objects.all().delete()

    path = mwasa_data_import().joinpath("tafsire").joinpath("m_tafseer_video.json")
    ext = ".flv"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
        data = data[2]["data"]
        sura_list = Sura.objects.all()
        res = []
        found = 0
        not_found = 0

        for _ in data:
            if not (_["FileName"] and ["SuraFromId"] and _["SuraFromId"] and _["SuraToId"]):
                continue
            file_name = f'{_["FileName"]}{ext}'
            oldf_path = get_path_tafsir_audio().joinpath(file_name)
            if not _["FileName"]:
                continue

            TAFSEER_ALQURAN_File = FilerFile.objects.filter(
                Q(file__icontains=_["FileName"]) | Q(original_filename__icontains=_["FileName"])
            ).first()
            if os.path.exists(oldf_path):
                found_file = found_file + 1
                # print(f"file exixt at {oldf_path} ")
                file = import_file(oldf_path, [AUDIOS, TAFSEER_ALQURAN])
                check_file_and_delete(oldf_path, file.path)

            elif TAFSEER_ALQURAN_File:
                file = TAFSEER_ALQURAN_File
                found = found + 1
            else:
                print(f"continue file TAFSEER_ALQURAN not found_File {_['FileName']} ")
                not_found = not_found + 1
                continue

            if _["SuraFromId"] != _["SuraToId"]:
                print(f'SuraToId{_["SuraToId"]}')
            suras = sura_list.filter(number__gte=val_if_none(_["SuraFromId"], 0), number__lte=val_if_none(_["SuraToId"], _["SuraFromId"])).all()
            sura_count = suras.count()

            for sura, idx in zip(suras, range(sura_count)):
                if sura_count == 1:
                    aya_start = Ayat.objects.filter(count=_["AyaFrom"], sura=sura).first()
                    aya_end = Ayat.objects.filter(count=_["AyaTo"], sura=sura).first()

                else:
                    if idx == 0:
                        aya_end = Ayat.objects.filter(sura=sura).last()
                        aya_start = Ayat.objects.filter(count=_["AyaFrom"], sura=sura).first()
                    elif idx == sura_count - 1:
                        aya_start = Ayat.objects.filter(sura=sura).first()
                        aya_end = Ayat.objects.filter(count=_["AyaTo"], sura=sura).first()
                    else:
                        aya_start = Ayat.objects.filter(sura=sura).first()
                        aya_end = Ayat.objects.filter(sura=sura).last()

                res.append(
                    AyatTafsirVideo(
                        video_tafsir=file,
                        sura=sura,
                        aya_start=aya_start,
                        aya_end=aya_end,
                        video_url=_["YouTubeVideoID"],
                    )
                )

        AyatTafsirVideo.objects.bulk_create(res, ignore_conflicts=True)
        print("found", found)
        print("not_found", not_found)


def audio_delete_and_reEnter():
    ext = ".flv"
    audio = AyatTafsirAudio.objects.all()
    audio.delete()
    path = mwasa_data_import().joinpath("tafsire").joinpath("m_tafseer_audio.json")
    res = []
    exist_count = 0
    not_exist_count = 0
    i_found = 0
    con_file = 0
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
        data = data[2]["data"]
        sura_list = Sura.objects.all()
        for _ in data:
            suras = sura_list.filter(number__gte=val_if_none(_["SuraFromId"], 0), number__lte=val_if_none(_["SuraToId"], 1000)).all()

            sura_count = suras.count()
            # file = FilerFile.objects.filter(Q(file__icontains=_["FileName"]) | Q(original_filename__icontains=_["FileName"])).first()
            file_name = f'{_["FileName"]}{ext}'
            oldf_path = get_path_tafsir_audio().joinpath(file_name)
            TAFSEER_ALQURAN_File = FilerFile.objects.filter(
                Q(file__icontains=_["FileName"]) | Q(original_filename__icontains=_["FileName"])
            ).first()
            if os.path.exists(oldf_path):
                found_file = found_file + 1
                # print(f"file exixt at {oldf_path} ")
                file = import_file(oldf_path, [AUDIOS, TAFSEER_ALQURAN])
                check_file_and_delete(oldf_path, file.path)

            elif TAFSEER_ALQURAN_File:
                file = TAFSEER_ALQURAN_File
            else:
                con_file += 1
                continue

            for sura, idx in zip(suras, range(len(suras))):
                if sura_count == 1:
                    aya_start = Ayat.objects.filter(count=_["AyaFrom"], sura=sura).first()
                    aya_end = Ayat.objects.filter(count=_["AyaTo"], sura=sura).first()

                else:
                    if idx == 0:
                        aya_end = Ayat.objects.filter(sura=sura).last()
                        aya_start = Ayat.objects.filter(count=_["AyaFrom"], sura=sura).first()
                    elif idx == sura_count - 1:
                        aya_start = Ayat.objects.filter(sura=sura).first()
                        aya_end = Ayat.objects.filter(count=_["AyaTo"], sura=sura).first()
                    else:
                        aya_start = Ayat.objects.filter(sura=sura).first()
                        aya_end = Ayat.objects.filter(sura=sura).last()
                print(f"idx,sura_count{idx},{sura_count} sura{sura}-aya_start{aya_start}-aya_end{aya_end}-sound_tafsir{file}")
                if file:
                    i_found += 1
                exist_el = AyatTafsirAudio(
                    sura=sura,
                    aya_start=aya_start,
                    aya_end=aya_end,
                    sound_tafsir=file,
                )
                res.append(exist_el)

        print("not_exist_count", not_exist_count)
        print("exist_count", exist_count)
        print("i_found", i_found)
        print("con_file", con_file)

        AyatTafsirAudio.objects.bulk_create(res, ignore_conflicts=True)


class Command(BaseCommand):
    def handle(self, **options):
        # audio_delete_and_reEnter()
        import_losed_data_tafsir_fix_video()
