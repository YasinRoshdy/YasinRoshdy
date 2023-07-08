import json
from base.management.commands.help import mwasa_data_import

from base.models import Ayat, Hadith
from django.core.management.base import BaseCommand
from mwasa2.settings import BASE_DIR
from filer.fields.file import FilerFileField


class Command(BaseCommand):
    def handle(self, **options):
        count = Ayat.objects.all().count()

        f = open(mwasa_data_import().joinpath("quran_text.json"), encoding="utf-8")
        data = json.load(f)

        lista = []

        data = data[2]["data"]
        print(len(data))
        all_ayat = Ayat.objects.all()
        for line in data:
            print(line)
            aya = all_ayat.get(sura__number=int(line["sura"]), count=line["aya"])
            aya.text_without_tashkil = line["text"]
            print(aya)
            print("*" * 20)
            lista.append(aya)

            pass
        # lista.append(_hadith_m)
        Ayat.objects.bulk_update(lista, fields=["text_without_tashkil"])

        print("original count", count)
        print("lista count", len(lista))
        f.close()
