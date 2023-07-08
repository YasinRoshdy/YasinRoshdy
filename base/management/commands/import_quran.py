# import json

# from base.models import Ayat, Hadith, Sura
# from django.core.management.base import BaseCommand
# from mwasa.settings import BASE_DIR

# import re


# class Command(BaseCommand):
#     def handle(self, **options):
#         first_digit = 0
#         secend_digit = 0

#         ayas: list[Ayat] = []
#         for i in range(114):
#             j = i + 1
#             # for i in range(10, 114):
#             if j > 9:
#                 secend_digit = ""

#             if j > 99:
#                 first_digit = ""

#             f = open(
#                 BASE_DIR.parent.parent.joinpath("data").joinpath("quran").joinpath(f"{first_digit}{secend_digit}{j}.txt"),
#                 encoding="utf-8",
#             )
#             sura = Sura.objects.get(number=j)
#             # if not sura:
#             #     sura = Sura(number=j)
#             # sura = Sura.objects.get(number=i + 1)
#             count = 0

#             for aya in f.readlines():
#                 count += 1
#                 aya = aya.strip()
#                 ayas.append(Ayat(sura=sura, text=aya, count=count))

#             sura.ayas_count = count
#             sura.save()

#             print(f"j:{j}|sura.number:{sura.number}|sura.ayas_count:{sura.ayas_count}")

#             # _hadith_m.save()

#             f.close()
#         Ayat.objects.bulk_create(ayas)


#
import json
import re
from base.management.commands.help import mwasa_data_import

from base.models import Ayat, Hadith, Sura
from django.core.management.base import BaseCommand
from mwasa2.settings import BASE_DIR


class Command(BaseCommand):
    def handle(self, **options):

        ayas: list[Ayat] = []
        file_name = mwasa_data_import().joinpath("quran-uthmani_sura_aya.txt")

        f = open(
            file_name,
            encoding="utf-8",
        )

        o_sura_num = -1
        sura: Sura
        sura_aya_count = 0

        for aya in f.readlines():

            val = aya.strip().split("|")

            sura_num = int(val[0])
            aya_num = int(val[1])
            text = val[2]

            print(sura_num)
            print(aya_num)
            print("====")
            aya = aya.strip()
            if o_sura_num != sura_num:
                sura = Sura.objects.get(number=sura_num)
                o_sura_num = sura_num
            if sura_aya_count < aya_num:
                sura_aya_count = aya_num

            ayas.append(Ayat(sura=sura, text=text, count=aya_num))

            # _hadith_m.save()
            # sura_list.append(sura)
        f.close()
        Ayat.objects.bulk_create(ayas)
        # Sura.objects.bulk_update(sura_list)
        pass
