from datetime import date
from logging import ERROR, Logger

# from base.general.logic.logic import PrayTime_parseJSON
# from base.models import PrayTime
import requests
import json

log = Logger("Base")


# def get_pray(city, country=None) -> PrayTime:
#     _date = date.today()
#     pray_today: PrayTime
#     pray_today = PrayTime.objects.filter(date=_date, city=city).all().first()

#     if not pray_today:
#         try:

#             # if True:

#             # her we can check if hadeth or .. are None then we can git the lase one of type
#             webUrl = requests.get(
#                 f"https://api.pray.zone/v2/times/today.json?city={city}")
#             # webUrl = requests.get("https://api.pray.zone/v2/times/today.json?city=cairo")
#             if webUrl.status_code == 200:
#                 _data = json.loads(webUrl.text)
#                 # _data = webUrl.json()

#                 pray_today = PrayTime_parseJSON(_data)
#                 pray_today.save()
#             else:
#                 raise Exception(
#                     f"M_BASE_Error:url https://api.pray.zone/v2/times/today.json?city={city} Status Code:{webUrl.status_code} {webUrl}"
#                 )

#         except Exception as e:

#             log.log(level=ERROR, msg=f"get_pray : try get api.pray.zone {e} ")
#             # pray_today = PrayTime.objects.filter(country=country, city=city).last()

#     return pray_today
