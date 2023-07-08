import json
import os
from pathlib import Path
from typing import Set

from base.management.commands.help import check_file_and_delete, mwasa_data_import
from base.management.commands.import_filer import AUDIOS, VIDEOS, get_path_audio, get_path_video, import_file
from base.management.commands.import_old_site_data_bukkhari import get_path_audio_Albokhary_file

from base.models import Ayat, BookInAlSaheh, ChapterInAlSaheh, Hadith, TafsirHadithInAlSaheh
from django.core.management.base import BaseCommand
from mwasa2.settings import BASE_DIR
from filer.models.filemodels import File as FilerFile


def handle_bukkhari_tafsir():
    ext_vid = ".flv"
    ext_aud = ".mp3"
    bukkhari = open(mwasa_data_import().joinpath("bukkhari").joinpath("bukkhari.json"), encoding="utf-8")
    data = json.load(bukkhari)
    data = data[2]["data"]
    books = {}
    babs = []

    tafsir_hadith_lista = []
    chapter_intro = ChapterInAlSaheh.objects.filter(id=1).first()
    book_intro = BookInAlSaheh.objects.filter(id=1).first()
    chapter_intro.name = "مقدمة في علم الحديث"
    chapter_intro.name_without_tashkil = "مقدمة في علم الحديث"
    chapter_intro.save()
    file_path_audio_count_exixt = 0
    file_path_video_count_exixt = 0

    file_path_audio_count = 0
    file_path_video_count = 0
    for _ in data:
        bab_name = _["bab"] if _["bab"] else _["babWithoutTashkeel"]

        chapter = ChapterInAlSaheh.objects.filter(name=bab_name).first()
        if not chapter:
            print(_)
        else:
            if not chapter.name_without_tashkil:

                chapter.name_without_tashkil = _["babWithoutTashkeel"] if _["babWithoutTashkeel"] else _["bab"]
                babs.append(chapter)

        # print(hadith.chapter.id)
        # hadith_lista.append(hadith)
        # ========
        item_hadith_tafsir_list = []
        files_lista = _["videoFile"].split("-")
        url_lista = _["YouTubeVideoID"].split(",")
        aud_file = _["sndFile"].strip().capitalize()
        # print("befor import_file audio", url, files_lista, url_lista)
        file_path_audio = get_path_audio_Albokhary_file(aud_file + ext_aud)
        # if not os.path.exists(file_path_audio):
        #     print(file_path_audio)
        #     file_path_audio_count = file_path_audio_count + 1
        # else:
        #     file_path_audio_count_exixt = file_path_audio_count_exixt + 1
        audio_added_once = False
        for file_n, url in zip(files_lista, url_lista):
            file_n = file_n.strip()
            url = url.strip()
            # if file == "" and url == "" and audio_added_once:
            #     continue
            file_n = file_n.strip() + ext_vid
            # file_path_video = get_path_video_Albokhary_file(file)
            # for audio
            # foldor = ["parent", "child"]

            # if not os.path.exists(file_path_video):
            #     print("file_path, url", file_path_video, url, _["id"])
            #     file_path_video_count = file_path_video_count + 1
            # else:
            #     file_path_video_count_exixt = file_path_video_count_exixt + 1
            # audio_added_once = True
            # continue

            file_audio = FilerFile.objects.filter(file__icontains=aud_file).first()
            file_video = FilerFile.objects.filter(file__icontains=file_n).first()
            # if os.path.exists(file_path_audio):

            #     file_audio = import_file(file_path_audio, [AUDIOS, "Albokhary"])
            #     check_file_and_delete(file_path_audio, file_audio.path)
            #     print("file_audio", file_audio)

            # if os.path.exists(file_path_video):
            #     file_video = import_file(file_path_video, [VIDEOS, "Albokhary"])
            #     check_file_and_delete(file_path_video, file_video.path)
            #     print("file_video", file_video)
            if not file_audio:
                print(f"file_audio {aud_file}")
                file_path_audio_count = file_path_audio_count + 1
            else:
                file_path_audio_count_exixt = file_path_audio_count_exixt + 1

            if not file_video:
                print(f"file_video {file_n}")

                file_path_video_count = file_path_video_count + 1
            else:

                file_path_video_count_exixt = file_path_video_count_exixt + 1
            hadith_tafsir = TafsirHadithInAlSaheh(
                book_id=_["ketab_id"] if _["ketab_id"] else book_intro.id,
                chapter=chapter if chapter else chapter_intro,
                hadith_id=_["id"],
                video_url=url,
                video_tafsir=file_video,
                audio_tafsir=file_audio,
            )
            item_hadith_tafsir_list.append(hadith_tafsir)

        tafsir_hadith_lista.extend(item_hadith_tafsir_list)

    print("not found count  audio ", file_path_audio_count)
    print("found count  audio", file_path_audio_count_exixt)

    print("not found count  video ", file_path_video_count)
    print("found count  video", file_path_video_count_exixt)
    TafsirHadithInAlSaheh.objects.bulk_create(tafsir_hadith_lista, ignore_conflicts=True)


class Command(BaseCommand):
    def handle(self, **options):
        # handle_bukkhari_books()
        # handle_bukkhari_bab()
        # handle_bukkhari()
        handle_bukkhari_tafsir()

        # TafsirHadithInAlSaheh()
