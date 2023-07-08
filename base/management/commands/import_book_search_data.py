import os
from base.management.commands.help import mwasa_data_import
from base.models import Ayat, Book, BookSeach
from django.core.management.base import BaseCommand

from mwasa2.settings import BASE_DIR


class Command(BaseCommand):
    def handle(self, **options):
        dir = mwasa_data_import().joinpath("book search").joinpath("book_search")

        lista = os.listdir(dir)
        print(lista)
        res = []
        for el in lista:
            with open(dir.joinpath(el), encoding="utf-8") as a:
                book = Book.objects.filter(title=el).first()
                print(book)
                if not book:
                    book = Book(title=el, type="book")
                    book.save()
                lines = a.readlines()
                for i in range(0, len(lines), 2):

                    print("i readline i , read line i+1", i, a.readline(i), a.readline(i + 1))
                    key = lines[i]
                    page_number = lines[i + 1]
                    print("a ,key,page_number", a, key, page_number)
                    if key == "" or page_number == "":
                        pass
                    else:
                        print(key, page_number)
                        res.append(BookSeach(key=key, page=int(page_number), book=book))

        BookSeach.objects.bulk_create(res)
