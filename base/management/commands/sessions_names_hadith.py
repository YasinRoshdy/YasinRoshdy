import json
from webbrowser import get
from base.management.commands.help import mwasa_data_import
from base.management.commands.set_sub_category_sessions import get_all_folder_name, get_last_folder_name

from base.models import SESSIONS_TYPE, Ayat, Hadith, Sessions, SessionsCategory, Sura
from django.core.management.base import BaseCommand
from mwasa2.settings import BASE_DIR
from filer.models.filemodels import File as FilerFile, Folder as FilerFoldor


class Command(BaseCommand):
    def handle(self, **options):

        # had_session = Sessions.objects.filter(type=SESSIONS_TYPE[1][0]).all()
        # found = 0
        # found_man = 0
        # found_man_exact = 0
        # found_man_not_exact = 0
        # loses = 0
        # with open(mwasa_data_import().joinpath("filenames_had_sessions.txt"), encoding="utf-8") as f:

        #     file_names = f.readlines()
        #     file_names = [el.strip() for el in file_names]
        #     # count = had_session.filter().all().count()
        #     for el in had_session:
        #         file = el.file
        #         folder = file.folder
        #         folder_name = get_last_folder_name(folder)

        #         cnt = file_names.count(folder_name)
        #         folder_count = FilerFoldor.objects.filter(name__icontains=folder_name).count()
        #         if cnt == 0:
        #             loses += 1
        #             print(folder_name)

        #         elif cnt == 1:
        #             found += 1

        #         else:
        #             # print(f"founded {cnt} {folder_name}")
        #             found_man += 1
        #             match = [el for el in file_names if folder_name in el]
        #             print(f"match {match}")
        #             print(f"FilerFoldor {FilerFoldor.objects.filter(name__icontains=folder_name).all()}")

        #             if folder_count == cnt:
        #                 found_man_exact += 1
        #             else:
        #                 found_man_not_exact += 1
        #                 # print(f"FilerFoldor {FilerFoldor.objects.filter(name__icontains=folder_name).all()}")

        # print(f"found {found}")
        # print(f"loses {loses}")
        # print(f"found_man {found_man}")

        # print(f"found_man_exact {found_man_exact}")
        # print(f"found_man_not_exact {found_man_not_exact}")

        had_session = Sessions.objects.filter(type=SESSIONS_TYPE[1][0]).all()
        found = 0
        found_man = 0
        found_man_exact = 0
        found_man_not_exact = 0
        loses = 0
        with open(mwasa_data_import().joinpath("filenames_had_sessions.txt"), encoding="utf-8") as f:

            file_names = f.readlines()
            file_names = [el.strip() for el in file_names]
            # count = had_session.filter().all().count()
            for el in had_session:
                file = el.file
                folder = file.folder
                folder_names = get_all_folder_name(folder)
                file_path = "/".join(folder_names)

                folder_name = folder_names[0]

                cnt = file_names.count(folder_name)

                folder_count = FilerFoldor.objects.filter(name__icontains=folder_name).count()
                if cnt == 0:
                    loses += 1
                    # print(f"loses{folder_name}")

                elif cnt == 1:
                    found += 1
                    match = [el for el in file_names if folder_name in el]
                    # print(f"match , {match}")
                    _max = ""
                    for _el in match:
                        if len(_el) > len(_max):
                            _max = _el
                    if _max.startswith("./"):
                        _max = _max[2:-1]
                    # book_name = None
                    # print(f"_max{_max}")
                    book_name = _max.split("/")[0].strip()

                    book_fnd = SessionsCategory.objects.filter(type="hadith", name=book_name).last()
                    if not book_fnd:
                        book_fnd = SessionsCategory(type="hadith", name=book_name).save()

                    el.category = book_fnd
                    el.save()

                else:

                    found_man += 1
                    match = [el for el in file_names if folder_name in el]
                    _count = match.count(folder_name)

                    i = 0
                    while i < _count:
                        match.remove(folder_name)
                        i += 1
                    dif_Base_names = []
                    for _it in match:
                        res = _it[2:].split("/")
                        dif_Base_names.append(res[2]) if len(res) > 2 else None

                    # if len(dif_Base_names) % 2 != 0:

                    #     found_man_exact += 1
                    #     print(f"dif_Base_names:{dif_Base_names}")
                    #     print(f"folder_names:{folder_names}")

                    #     folder_names

                    # else:
                    #     found_man_not_exact = found_man_not_exact + 1
                    #     # print(f"folder_names:{folder_names}")
                    #     # print(f"folder_name:{folder_name}")

                    if folder_count == cnt:
                        found_man_exact += 1
                        print(f"folder_count {folder_count}")

                    else:
                        found_man_not_exact += 1
                        print(f"folder_name:{folder_name}")
                        # print(f"FilerFoldor {FilerFoldor.objects.filter(name__icontains=folder_name).all()}")

        print(f"found {found}")
        print(f"loses {loses}")
        print(f"found_man {found_man}")

        print(f"found_man_exact {found_man_exact}")
        print(f"found_man_not_exact {found_man_not_exact}")
