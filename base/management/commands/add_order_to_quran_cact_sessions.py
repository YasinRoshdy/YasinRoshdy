import json
import re

from base.models import Ayat, Hadith, SessionsCategory, Sura
from django.core.management.base import BaseCommand
from mwasa2.settings import BASE_DIR


class Command(BaseCommand):
    def handle(self, **options):
        res = []

        categ = SessionsCategory.objects.filter(type="quran").all()
        for el in categ:
            el.order = None
            res.append(el)

        SessionsCategory.objects.bulk_update(res, fields=["order"])

        res = []
        exixst = 0
        for cat in categ:
            sura = Sura.objects.filter(name__iexact=cat.name.split("-")[0]).first()

            if sura:
                exixst += 1
                cat.order = sura.number

                res.append(cat)

        # print(f"exixst {exixst }")
        SessionsCategory.objects.bulk_update(res, fields=["order"])
