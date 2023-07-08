import json
import os
from pathlib import Path
from typing import Set
from django.core.management.base import BaseCommand
from mwasa2.settings import BASE_DIR
from django.db import models
from isort import file
from base.management.commands.help import check_file_and_delete, mwasa_content, mwasa_data_import
from base.management.commands.import_filer import AUDIOS, VIDEOS, get_path_audio, get_path_video, import_file
from filer.models.filemodels import File as FilerFile, Folder as FilerFoldor


class Command(BaseCommand):
    def handle(self, **options):

        filers = FilerFile.objects.all()
        for filer_item in filers:
            if not os.path.exists(filer_item.path):
                filer_item.delete()
