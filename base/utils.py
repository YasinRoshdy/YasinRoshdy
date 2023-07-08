import PyPDF2
from django.db import models


def get_page_count_pdf(pdf_path):
    pg_count = -1
    with open(f"{pdf_path}", "rb") as file:
        readpdf = PyPDF2.PdfFileReader(file)
        pg_count = readpdf.numPages

    return pg_count


class BookQuerySet(models.query.QuerySet):
    def update_page_count_instance(self, data, instanceType):
        def get_updated_book(_book: instanceType):
            if not _book.page_count and _book.file and "pdf" in _book.file.mime_type:
                print(f"path {_book.file.file.path}")
                page_c = get_page_count_pdf(_book.file.file.path)

                _book.page_count = page_c
            return _book

        # if isinstance(data, list):
        #     books = [get_updated_book(book) for book in data]

        #     instanceType.objects.bulk_update(books, ["page_count"])
        # else:
        book = get_updated_book(data)
        book.save()

    def get(self, **kwargs):
        print("get  BookQuerySet")
        instance = super().get(**kwargs)
        self.update_page_count_instance(instance, type(instance))

        return super().get(**kwargs)

    def all(self, **kwargs):
        lista = super().all(**kwargs)

        for el in lista:
            self.update_page_count_instance(el, type(el))

        return lista


class BookManager(models.Manager.from_queryset(BookQuerySet)):
    pass
