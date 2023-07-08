from base.models import SESSIONS_TYPE, Sessions, SessionsCategory
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):
        # sessions = Sessions.objects.all()
        # cats = []
        # for el in sessions:
        #     if el.category:
        #         cat = el.category
        #         cat.type = el.type
        #         cats.append(cat)

        # SessionsCategory.objects.bulk_update(cats, ["type"])

        lista = SessionsCategory.objects.all()
        for el in lista:
            print(f"{el.name} {el.type}")
