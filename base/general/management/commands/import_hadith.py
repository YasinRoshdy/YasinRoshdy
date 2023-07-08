# import json

# from base.models import Hadith
# from django.core.management.base import BaseCommand
# from mwasa2.settings import BASE_DIR


# class Command(BaseCommand):
#     def handle(self, **options):

#         f = open(BASE_DIR.parent.parent.joinpath("data").joinpath("bukhari.json"), encoding="utf-8")
#         data = json.load(f)

#         lista = []
#         for hadith in data:
#             text = hadith["hadith"]
#             number = hadith["number"]
#             description = hadith["description"]
#             searchTerm = hadith["searchTerm"]
#             _hadith_m = Hadith.objects.create(text=text, number=number, description=description, searchTerm=searchTerm)
#             lista.append(_hadith_m)

#         Hadith.objects.bulk_create(lista)
#         f.close()
