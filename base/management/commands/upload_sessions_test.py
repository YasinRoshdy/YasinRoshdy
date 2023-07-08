from base.management.commands.youtube.start import upload_list
from base.models import SESSIONS_TYPE, Sessions, SessionsCategory
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _


def upload_item(path, type, category):
    pass


class Command(BaseCommand):
    def handle(self, **options):
        my_type = "quran"
        sessions_category = SessionsCategory.objects.all()
        mycat = sessions_category.filter(type=my_type, name="الفاتحة").first()

        sessions = Sessions.objects.filter(category=mycat).all()
        upload_lista = []
        name_of_playlist = f"{_('Sessions')} / {SESSIONS_TYPE[0][1]} / {mycat.name}"

        for session in sessions:
            # url = upload_item(session.file.file, mycat.type, mycat.name)

            def save_new_session(youtube_url):
                session.video_url = youtube_url
                session.save()

            upload_lista.append(
                {
                    # "func": save_new_session,
                    "file": session.file.path,
                    "session": session,
                    "category": session.category,
                }
            )

        desc = ""
        upload_list(upload_lista, name_of_playlist, desc)
