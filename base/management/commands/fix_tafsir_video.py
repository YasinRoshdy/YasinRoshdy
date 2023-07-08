from re import A
from base.models import AyatTafsirVideo

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):
        ayat = AyatTafsirVideo.objects.filter(sura=None).all()
        for el in ayat:
            el.sura = (
                el.aya_start.sura if (el.aya_start and el.aya_start.sura) else el.aya_end.sura if el.aya_end and el.aya_end.sura else None
            )

        AyatTafsirVideo.objects.bulk_update(ayat, ["sura"])
