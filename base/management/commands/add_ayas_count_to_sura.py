import json
import re

from base.models import Ayat, Hadith, Sura
from django.core.management.base import BaseCommand
from mwasa2.settings import BASE_DIR


class Command(BaseCommand):
    def handle(self, **options):
        suras = Sura.objects.all()
        for sura in suras:

            ayas_count = Ayat.objects.filter(sura=sura.id).all().count()
            sura.ayas_count = ayas_count

        Sura.objects.bulk_update(suras, fields=["ayas_count"])
