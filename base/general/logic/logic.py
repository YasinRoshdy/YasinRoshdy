from datetime import date, datetime, time
from sqlite3 import Time
from time import strftime

import PyPDF2
from base.general.logic.general import en_to_ar

from base.models import DailyPublish, General_information, RelatedSites  # PrayTime,


from django.contrib.sessions.models import Session


arabic_months_order = """
محرم 
صفر	 
ربيع الأول	 
ربيع الثاني	 
جمادى الأولى	 
جمادى الأخرة	 
رجب	 
شعبان	 
رمضان	 
شوال	 
ذو القعدة	 
ذو الحجة
"""


def from_month_number_to_name(month):
    return arabic_months_order.split("\n")[int(month)].strip()


def hijri_converter(_date: str):
    # 1443-07-26

    res = _date.split("-")

    res[1] = from_month_number_to_name(res[1])
    # print(res)
    return "-".join(res)


def from_datetimestr_to_time(value):
    value = is_val(value)
    if not value:
        return None

    time_format = "%H:%M"
    return datetime.strptime(value, time_format).time()


def format_time(time: Time):
    if time:

        # return strftime("%H:%M")
        return f"{time.hour}:{time.minute}"


# {
#     "code": 200,
#     "status": "OK",
#     "results": {
#         "datetime": [
#             {
#                 "times": {
#                     "Imsak": "05:24",
#                     "Sunrise": "06:59",
#                     "Fajr": "05:34",
#                     "Dhuhr": "12:10",
#                     "Asr": "15:02",
#                     "Sunset": "17:22",
#                     "Maghrib": "17:37",
#                     "Isha": "18:46",
#                     "Midnight": "23:28",
#                 },
#                 "date": {"timestamp": 1642291200, "gregorian": "2022-01-16", "hijri": "1443-06-13"},
#             }
#         ],
#         "location": {
#             "latitude": 31.200092315673828,
#             "longitude": 29.918739318847656,
#             "elevation": 14.0,
#             "city": "Alexandria",
#             "country": "Egypt",
#             "country_code": "EG",
#             "timezone": "Africa/Cairo",
#             "local_offset": 2.0,
#         },
#         "settings": {
#             "timeformat": "HH:mm",
#             "school": "Ithna Ashari",
#             "juristic": "Shafii",
#             "highlat": "None",
#             "fajr_angle": 18.0,
#             "isha_angle": 18.0,
#         },
#     },
# }
# [
#     {
#         "times": {
#             "Imsak": "05:24",
#             "Sunrise": "06:59",
#             "Fajr": "05:34",
#             "Dhuhr": "12:10",
#             "Asr": "15:02",
#             "Sunset": "17:22",
#             "Maghrib": "17:37",
#             "Isha": "18:46",
#             "Midnight": "23:28",
#         },
#         "date": {"timestamp": 1642291200, "gregorian": "2022-01-16", "hijri": "1443-06-13"},
#     }
# ]


# 'Imsak':'05:22'
# 'Sunrise':'06:44'
# 'Fajr':'05:32'
# 'Dhuhr':'12:34'
# special variables
# function variables
# 0:{'times': {'Imsak': '05:22', 'Sunrise': '06:44', 'Fajr': '05:32', 'Dhuhr': '12:34', 'Asr': '15:54', 'Sunset': '18:25', 'Maghrib': '18:36', 'Isha': '-', 'Midnight': '23:59'}, 'date': {'timestamp': 1645488000, 'gregorian': '2022-02-22', 'hijri': '1443-07-21'}}
# special variables
# function variables
# 'times':{'Imsak': '05:22', 'Sunrise': '06:44', 'Fajr': '05:32',
# 'Dhuhr': '12:34', 'Asr': '15:54',
# 'Sunset': '18:25', 'Maghrib': '18:36',
# 'Isha': '-', 'Midnight': '23:59'}
# 'Asr':'15:54'
# 'Sunset':'18:25'
# 'Maghrib':'18:36'
# 'Isha':'-'
# 'Midnight':'23:59'
def is_val(val):
    return val if "-" not in val else None


# def PrayTime_parseJSON(json_data):
#     _datetime = json_data["results"]["datetime"][0]["times"]

#     obj: PrayTime = PrayTime(
#         Fajr=from_datetimestr_to_time(_datetime["Fajr"]),
#         Sunrise=from_datetimestr_to_time(_datetime["Sunrise"]),
#         Dhuhr=from_datetimestr_to_time(_datetime["Dhuhr"]),
#         Maghrib=from_datetimestr_to_time(_datetime["Maghrib"]),
#         Isha=from_datetimestr_to_time(_datetime["Isha"]),
#         Asr=from_datetimestr_to_time(_datetime["Asr"]),
#         city=json_data["results"]["location"]["city"],
#         country=json_data["results"]["location"]["country"],
#         date=date.today(),
#         hijri=hijri_converter(json_data["results"]["datetime"][0]["date"]["hijri"]),
#     )
#     return obj


def to_url(url):
    if not url:
        return url
    pref = "https://www.youtube.com/watch?v="
    if pref not in url:
        return pref + url

    return url


def youtube_url(url: str):
    if not url:
        return None
    if "watch?v=" in url:
        return url.replace("watch?v=", "embed/")
    elif "embed/" in url:
        return url

    else:
        return youtube_url(to_url(url))


def basic_info():
    general = General_information.objects.last()

    result = {}

    if general:
        result = {
            "visitor_count": get_visitor_count(),
            "instagram_link": general.instagram_link,
            "facebook_link": general.facebook_link,
            "twitter_link": general.twitter_link,
            "youtube_link": general.youtube_link,
            "related_sites": RelatedSites.objects.filter(),
        }
        # if site:
        result["cover_page"] = general.cover_page
        result["about_mousa"] = general.about_mousa
        result["about_sheikh"] = general.about_sheikh
        result["cover_theme"] = general.about_sheikh

    return result


def get_daily_publish():
    _date = date.today()

    data = {}
    # daily = DailyPublish.objects.filter(day=_date.day, status="p").first()
    daily = DailyPublish.objects.filter(display_date= _date,status="p").all()

    hadith = daily.filter(publish_type="hadith").last()
    aya = daily.filter(publish_type="aya").last()
    fatwa = daily.filter(publish_type="fatwa").last()
    part_of_book = daily.filter(publish_type="part_of_book").last()

    if hadith is not None:
        data["hadeth"] = hadith.hadith.text
    if aya is not None:
        data["aya"] = aya.aya.text
    if fatwa is not None:
        data["fatwa"] = fatwa.content
    if part_of_book is not None:
        data["part_of_book"] = part_of_book.content

    return data


def get_visitor_count():

    return Session.objects.all().count()


def prepare_str(val: str):
    if not val or not isinstance(val, str):
        return val

    else:
        # val = val.strip()

        return val.strip().replace("\n", " ").replace("\r", "")


def from_ayat_to_text(ayat, number, igone_besm_start=True):

    if number == 1 and igone_besm_start:
        ayat = ayat[1:]
    concat = ""
    # if self.name != "الفاتحة" or self.name != "التوبَة":
    #     concat = Ayat.objects.all().first().text + "\n"

    for aya in ayat:
        c = en_to_ar(aya.count)
        concat += f"{aya.text}<span>﴿{c}﴾</span>"

    return concat
