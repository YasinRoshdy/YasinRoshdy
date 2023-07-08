import json
from webbrowser import get
from base.management.commands.help import mwasa_data_import

from base.models import Ayat, Hadith, Sura
from django.core.management.base import BaseCommand
from mwasa2.settings import BASE_DIR


class Command(BaseCommand):
    def handle(self, **options):
        suras = Sura.objects.all()
        for el in suras:
            el.delete()

        f = open(mwasa_data_import().joinpath("quran").joinpath("meta.txt"), encoding="utf-8")
        i = 1
        for line in f.readlines():
            res: list[str] = line.split("	")
            name: str = res[0].strip()
            name = name.strip().removeprefix("سورة").removesuffix("سورة").strip()
            # loc = res[1].strip()
            # sura = Sura.objects.get(name=name)

            # if sura:
            #     sura.number = i

            # else:
            sura = Sura(name=name, number=i)
            sura.save()

            i += 1
        # _hadith_m.save()

        f.close()
