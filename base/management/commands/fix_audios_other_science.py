import json
import os
from django.core.management.base import BaseCommand

from base.management.commands.help import check_file_and_delete, mwasa_data_import
from base.management.commands.import_filer import AUDIOS, import_file
from base.management.commands.import_other_science import RAMADANIAT, get_ramadaniat_audio_Path
from base.models import MEDIA_TYPE, OtherScience, OtherScienceSubject


def fix_ramadaniat_audio():
    with open(mwasa_data_import().joinpath(RAMADANIAT).joinpath("audio.json"), encoding="utf-8") as f:
        data = json.load(f)
        data = data[2]["data"]

        ext = ".mp3"
        base_path = get_ramadaniat_audio_Path()

        others = []
        for _ in data:

            # print("_", _)
            catg = _["catg"].strip()
            subject = OtherScienceSubject.objects.filter(subjects=catg, file_type=MEDIA_TYPE[1][0]).first()
            if not subject:
                subject = OtherScienceSubject(file_type=MEDIA_TYPE[1][0], subjects=catg)
                # subjects.append(subject)
                subject.save()
            other_science = OtherScience.objects.filter(title=_["title"], subject=subject).first()
            if not other_science:

                oldf_path = base_path.joinpath(_["folder"]).joinpath(f'{_["filename"]}{ext}')
                if os.path.exists(oldf_path):
                    file = import_file(oldf_path, [AUDIOS, RAMADANIAT, _["folder"]])
                    check_file_and_delete(oldf_path, file.path)

                others.append(OtherScience(title=_["title"], file=file, subject=subject))

        # OtherScienceSubject.objects.bulk_create(subjects)
        OtherScience.objects.bulk_create(others)


class Command(BaseCommand):
    def handle(self, **options):

        # import_ramadaniat_audio()
        fix_ramadaniat_audio()
