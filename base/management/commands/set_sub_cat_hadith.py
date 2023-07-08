import os
from base.management.commands.help import check_file_and_delete
from base.management.commands.import_filer import VIDEOS, import_file
from base.management.commands.import_sessions_ramadaniat import DIR_NAME, SESSIONS, import_sessions_ramadaniat_path
from base.models import SESSIONS_TYPE, Sessions, SessionsCategory
from django.core.management.base import BaseCommand


_type = SESSIONS_TYPE[2][0]  # quran

exixt = 0
not_exixt = 0


def import_ramadaniat_hadith():

    base_path = import_sessions_ramadaniat_path()
    print("base_path", base_path)
    lista_subjects = os.listdir(base_path)
    sessions = []
    file_not_exixt = 0
    file_exixt = 0
    all = 0
    for book in lista_subjects:
        # print("sura", sura)
        # print(base_path.joinpath(sura))
        book_dirs_names = os.listdir(base_path.joinpath(book))

        for dir_name in book_dirs_names:
            dir_name_path = base_path.joinpath(book).joinpath(dir_name)

            if os.path.isdir(dir_name_path):

                files_in_dir = os.listdir(dir_name_path)
                for file_name in files_in_dir:
                    # this may be file or dir

                    file_path = base_path.joinpath(book).joinpath(dir_name).joinpath(file_name)
                    if os.path.isdir(file_path):
                        lista_in_sub_dir = os.listdir(file_path)
                        for item_in_sub_dir in lista_in_sub_dir:
                            item_in_sub_dir_path = base_path.joinpath(book).joinpath(dir_name).joinpath(file_name).joinpath(item_in_sub_dir)

                            if os.path.isdir(item_in_sub_dir_path):
                                lista_in_sub_sub_dir = os.listdir(item_in_sub_dir_path)
                                for item_in_sub_sub_dir in lista_in_sub_sub_dir:
                                    item_in_sub_sub_dir_path = (
                                        base_path.joinpath(book)
                                        .joinpath(dir_name)
                                        .joinpath(file_name)
                                        .joinpath(item_in_sub_dir)
                                        .joinpath(item_in_sub_sub_dir)
                                    )
                                    import_item(
                                        item_in_sub_sub_dir_path,
                                        item_in_sub_sub_dir,
                                        [VIDEOS, SESSIONS, DIR_NAME, dir_name, file_name, item_in_sub_dir, item_in_sub_sub_dir],
                                    )

                            else:
                                import_item(
                                    item_in_sub_dir_path, item_in_sub_dir, [VIDEOS, SESSIONS, DIR_NAME, dir_name, file_name, item_in_sub_dir]
                                )

                    else:
                        import_item(file_path, file_name, [VIDEOS, SESSIONS, DIR_NAME, dir_name, file_name])
            else:
                import_item(dir_name_path, dir_name, [VIDEOS, SESSIONS, DIR_NAME, book])

            # sessions.append(Sessions(file=file, title=file_name, type=type).save())

    # Sessions.objects.bulk_create(sessions)
    print("exixt", exixt)
    print("nott exixt", not_exixt)


def print_item(file_path, file_name, dirs_list):
    global exixt
    global not_exixt
    if os.path.exists(file_path):
        print("exixt", file_path, "dirs lista ", dirs_list)
        exixt = exixt + 1
    else:
        print("not exixt", file_path, "dirs lista ", dirs_list)
        not_exixt = not_exixt + 1


def import_item(file_path, file_name, dirs_list):

    global exixt
    global not_exixt
    global _type
    if os.path.isfile(file_path):
        print("is file , ", file_path)
        exixt = exixt + 1

        file = import_file(file_path, dirs_list)
        check_file_and_delete(file_path, file.path)

        Sessions(file=file, title=os.path.basename(file_name), type=_type).save()
        print("added")
    else:
        not_exixt = not_exixt + 1


class Command(BaseCommand):
    def handle(self, **options):
        pass
