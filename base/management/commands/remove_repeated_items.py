from io import FileIO
from pathlib import Path
from base.management.commands.help import mwasa_content

from base.models import Ayat, AyatTafsirVideo, Sura
from django.core.management.base import BaseCommand
from django.core.files import File as DjangoFile

from filer.models.filemodels import File as FilerFile, Folder
from filer.management.commands.import_files import FileImporter

from mwasa2.settings import BASE_DIR


# # p_Audios='Audios'
# # p_Videos='Audios'
def delete_repeated():
    tafsirs = Ayat.objects.order_by("sura", "count").all().reverse()
    all_count = tafsirs.count()

    should_del = 0
    lista_repeated = []
    for tafsir in tafsirs:
        elems = tafsirs.filter(
            sura=tafsir.sura,
            count=tafsir.count,
        )
        print("elems", elems)
        if elems.count() > 1:

            # lista_repeated.append(tafsir)
            tafsir.delete()
            should_del += 1

    print("all", all_count)
    print("should delete", should_del)


# def make_repeated():
#     items = AyatTafsirVideo.objects.all()

#     lista = []
#     for item in items:

#         lista.append(
#             AyatTafsirVideo(
#                 sura=item.sura, aya_start=item.aya_start, aya_end=item.aya_end, video_tafsir=item.video_tafsir, video_url=item.video_url
#             )
#         )

#     AyatTafsirVideo.objects.bulk_create(lista)


class Command(BaseCommand):
    def handle(self, **options):

        # make_repeated()
        delete_repeated()
        # Ayat.objects.all().delete()
