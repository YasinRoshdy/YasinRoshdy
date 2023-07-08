import json
import re

from base.models import Ayat, Hadith, Sessions, Sura
from django.core.management.base import BaseCommand
from mwasa2.settings import BASE_DIR


class Command(BaseCommand):
    def handle(self, **options):
        sessions = Sessions.objects.all()
        res = []
        for el in sessions:
            print(el)

            print(el.title)
            if ".mp4" in el.title:
                print(el.title)
                el.title = el.title.replace(".mp4", "")
                print(el.title)

                res.append(el)

        Sessions.objects.bulk_update(res, fields=["title"])
