from base.models import SESSIONS_TYPE, Sessions, SessionsCategory
from django.core.management.base import BaseCommand


def get_last_folder_name(folder):

    name = folder.name
    prev = folder
    while folder.parent != None and "شرح البخارى والاسئلة MP4 مجالس" not in folder.name:
        prev = folder
        folder = folder.parent
    name = prev.name

    return name.strip()


def get_all_folder_name(folder):

    name = folder.name
    res = []
    res.append(folder.name.strip())
    while folder.parent != None and "شرح البخارى والاسئلة MP4 مجالس" not in folder.name:
        folder = folder.parent
        res.append(folder.name.strip())

    return res[::-1][1:]


def add_sub_cat_by_id(id):
    session_quran_lista = Sessions.objects.filter(type=SESSIONS_TYPE[id][0]).all()
    lista = []
    for el in session_quran_lista:
        file = el.file
        folder = file.folder
        folder_name = get_last_folder_name(folder)
        print(folder_name)
        continue

        print(f"folder {folder} {folder.name}")

        category = SessionsCategory.objects.filter(name=folder_name).first()
        if not category:

            category = SessionsCategory(name=folder_name)
            category.save()

        el.category = category

        lista.append(el)

    Sessions.objects.bulk_update(lista, ["category"])


def add_to_quran():
    add_sub_cat_by_id(0)


def add_to_hadith():
    add_sub_cat_by_id(1)


def add_to_ramadaniat():
    add_sub_cat_by_id(2)


class Command(BaseCommand):
    def handle(self, **options):

        add_to_hadith()
