from datetime import datetime
import json
from webbrowser import get
from base.management.commands.help import mwasa_data_import

from base.models import Ayat, Hadith, Sura
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):

        suras_list = []

        f = open(mwasa_data_import().joinpath("quran meta with loc.txt"), encoding="utf-8")
        i = 1
        for line in f.readlines():
            res: list[str] = line.split("	")
            name = res[0].strip()
            loc = res[1].strip()
            # sura = Sura.objects.get(name=name)

            # if sura:
            #     sura.number = i

            # else:
            print(f"number {i}")
            sura = Sura.objects.filter(number=i).first()
            sura.location = loc

            suras_list.append(sura)
            i += 1
        # _hadith_m.save()
        Sura.objects.bulk_update(suras_list, ["location"])

        f.close()
