from datetime import date
import sys
from base.general.logic.general import en_to_ar
from base.general.logic.logic import get_visitor_count, hijri_converter
from base.models import General_information, RelatedSites
from django.utils.safestring import SafeString
from hijri_converter import Hijri, Gregorian


def basic_info(request):
    _date = date.today()
    general = General_information.objects.first()
    # pray_today = PrayTime.objects.filter(date=_date).all().first()
    # hijri: str = pray_today.hijri

    hijri: str = Gregorian(_date.year, _date.month, _date.day).to_hijri()
    result = {}

    if general:
        result = {
            "visitor_count": get_visitor_count(),
            "instagram_link": general.instagram_link,
            "twitter_link": general.twitter_link,
            "youtube_link": general.youtube_link,
            "facebook_link": general.facebook_link,
            "google_play_link": general.google_play_link,
            "app_store_link": general.app_store_link,
        }
        # if site:
        result["cover_page"] = general.cover_page

        result["about_mousa_short"] = SafeString(general.about_mousa_short)
        result["about_sheikh_short"] = SafeString(general.about_sheikh_short)

        result["about_mousa"] = SafeString(general.about_mousa)
        result["about_sheikh"] = SafeString(general.about_sheikh)
    _hijri = en_to_ar(hijri)
    _hijri = hijri_converter(_hijri)
    _hijri = _hijri.split("-")

    result["hijri"] = _hijri[2] + " / " + _hijri[1] + " / " + _hijri[0]

    return {"info": result}
