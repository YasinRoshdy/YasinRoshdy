from io import FileIO
from pathlib import Path
from base.management.commands.help import mwasa_content

from base.models import Ayat
from django.core.management.base import BaseCommand
from django.core.files import File as DjangoFile

from filer.models.filemodels import File as FilerFile, Folder
from filer.management.commands.import_files import FileImporter

from mwasa2.settings import BASE_DIR


import ntpath


def _import_filer(path, foldor_list: list):  # list of nested foldor  the first is the direct parentt

    importer = FileImporter()
    foldor = importer.get_or_create_folder(foldor_list)

    file_obj = ntpath.basename(path)

    dj_file = DjangoFile(open(path, mode="rb"), name=file_obj)
    return importer.import_file(dj_file, foldor)


def import_file(path, foldor):
    return _import_filer(BASE_DIR.parent.joinpath("content").joinpath(path), foldor)


def get_path_audio():
    return mwasa_content().joinpath(AUDIOS)


def get_path_video():
    return mwasa_content().joinpath(VIDEOS)


AUDIOS = "Audios"
VIDEOS = "Videos"

# p_Audios='Audios'
# p_Videos='Audios'
class Command(BaseCommand):
    def handle(self, **options):
        foldor = ["parent", "child"]
        # and the file will put in child
        path = Path("temp").joinpath("file1.temp")
        # os.path.split("/tmp/d/a.dat")
        import_file(path, foldor)
