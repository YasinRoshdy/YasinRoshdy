import json
from pathlib import Path
from typing import Set

from base.management.commands.help import mwasa_data_import
from base.management.commands.import_filer import AUDIOS, VIDEOS, get_path_audio, get_path_video, import_file
from base.management.commands.import_quran_tafsire_telawa import tafseer_audio

from base.models import Ayat, BookInAlSaheh, ChapterInAlSaheh, Hadith, TafsirHadithInAlSaheh
from django.core.management.base import BaseCommand
from mwasa2.settings import BASE_DIR


class Command(BaseCommand):
    def handle(self, **options):
        tafseer_audio()
