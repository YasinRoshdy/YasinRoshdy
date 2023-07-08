from base.models import Ayat
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):

        r_str = "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ"
        r_str_without = "بسم الله الرحمن الرحيم"
        f_ayat = Ayat.objects.filter(count=1).all()
        f_ayat = f_ayat.exclude(sura__number=1).exclude(sura__number=9)

        for aya in f_ayat:
            aya.text = aya.text.replace(r_str, "").strip()
            aya.text_without_tashkil = aya.text.replace(r_str_without, "").strip()

        f_ayat.bulk_update(f_ayat, ["text", "text_without_tashkil"])
