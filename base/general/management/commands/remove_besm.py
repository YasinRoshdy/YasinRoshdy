from base.models import Ayat
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):

        r_str = "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ"
        f_ayat = Ayat.objects.filter(count=1).all()
        f_ayat = f_ayat.exclude(sura_id=454).exclude(sura_id=462)

        for aya in f_ayat:
            aya.text = aya.text.replace(r_str, "").strip()

        f_ayat.bulk_update(f_ayat, ["text"])
