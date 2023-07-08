from rest_framework import generics
from rest_framework.response import Response as ResponseRest
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
import json
from datetime import date, datetime
from logging import ERROR as L_ERROR
from logging import Logger
from django.utils.safestring import SafeString


from django import urls
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.paginator import Paginator
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView

from django.template.loader import render_to_string
from django.http import JsonResponse
from base.general.logic.general import get_title_url, if_val, remove_None_vals

from base.general.logic.logic import format_time, from_ayat_to_text, get_daily_publish, get_visitor_count, youtube_url
from base.general.logic.orm import get_file_data
from rest_framework.views import APIView
from .serializer import BookSeachSerializer, BookSerializer, OtherScienceSerializer, \
    FatwaSerializer, AyatNameSerializer, HadithNameSerializer
from django.shortcuts import render

# , get_pray
from base.models import (
    DAILY_PUBLISH_CHOICES,
    PHONE_NUMBER_TYPE,
    STATUS_PUBLISHED,
    AyatTafsirAudio,
    AyatTafsirVideo,
    AyatTelawa,
    Book,
    BookSeach,
    SessionsCategory,
)  # AlSaheh,
from base.models import (
    SESSIONS_TYPE,
    Ayat,
    # AyatTafsir,
    BookInAlSaheh,
    CallUs,
    ChapterInAlSaheh,
    DailyPublish,
    Email,
    Fatwa,
    General_information,
    Hadith,
    OtherScience,
    OtherScienceSubject,
    PhoneNumbers,
    # PrayTime,
    RelatedSites,
    Sessions,
    Sura,
    TafsirHadithInAlSaheh,
)

log = Logger("Base")
HOME_ID = 1
QURAN_ID = 2
HADITH_ID = 3
OTHER_SCIENCE_ID = 4
BOOKS_ID = 5
FATWA_ID = 6
SESSION_ID = 7
CALLUS_ID = 8
OTHER_SCIENCE_AUDIO_ID = 9
OTHER_SCIENCE_VIDEO_ID = 10
MAJALIS_QURAN_ID = 11
MAJALIS_HADITH_ID = 12
MAJALIS_OTHER_SCIENCE_ID = 13
PILLARS_ID = 14

# HOME_ICON = static("icons/active/home.svg")
# QURAN_ICON = static("icons/active/quran.svg")
# HADITH_ICON = static("icons/active/had.svg")
# OTHER_SCIENCE_ICON = static("icons/active/other.svg")
# BOOKS_ICON = static("icons/active/books.svg")
# FATWA_ICON = static("icons/active/fatwa.svg")
# SESSION_ICON = static("icons/active/sessions.svg")
# CALLUS_ICON = static("icons/active/call.svg")
# SEARCH_ICON = static("icons/search.svg")


HOME_ICON = static("image/logo.png")
QURAN_ICON = static("image/logo.png")
HADITH_ICON = static("image/logo.png")
OTHER_SCIENCE_ICON = static("image/logo.png")
BOOKS_ICON = static("image/logo.png")
FATWA_ICON = static("image/logo.png")
SESSION_ICON = static("image/logo.png")
CALLUS_ICON = static("image/logo.png")
SEARCH_ICON = static("image/logo.png")


# pagination constants
items_per_page = 26


def home(request):

    daily = get_daily_publish()
    # _date = date.today()

    data = {}

    # pray_today: PrayTime
    # pray_today = PrayTime.objects.filter(date=_date, city="Alexandria").all().first()
    # pray_data = {
    #     "Alexandria": {"country": "Egypt"},
    # }

    # if not pray_today:
    #     try:

    #         # if True:

    #         # her we can check if hadeth or .. are None then we can git the lase one of type
    #         webUrl = requests.get("https://api.pray.zone/v2/times/today.json?city=Alexandria")
    #         # webUrl = requests.get("https://api.pray.zone/v2/times/today.json?city=cairo")
    #         if webUrl.status_code == 200:
    #             _data = json.loads(webUrl.text)
    #             # _data = webUrl.json()

    #             pray_today = PrayTime_parseJSON(_data)
    #             pray_today.save()
    #         else:
    #             raise Exception(
    #                 f"M_Error:url https://api.pray.zone/v2/times/today.json?city=Alexandria Status Code:{webUrl.status_code} {webUrl}"
    #             )

    #     except Exception as e:

    #         log.log(level=L_ERROR, msg=f"in home : try get api.pray.zone {e} ")
    #         pray_today = PrayTime.objects.filter(city="Alexandria").last()
    # if pray_today:
    #     pray_data["Alexandria"]["Fajr"] = format_time(pray_today.Fajr)
    #     pray_data["Alexandria"]["Sunrise"] = format_time(pray_today.Sunrise)
    #     pray_data["Alexandria"]["Dhuhr"] = format_time(pray_today.Dhuhr)
    #     pray_data["Alexandria"]["Asr"] = format_time(pray_today.Asr)
    #     pray_data["Alexandria"]["Maghrib"] = format_time(pray_today.Maghrib)
    #     pray_data["Alexandria"]["Isha"] = format_time(pray_today.Isha)

    # data["pray_data"] = pray_data
    data["daily"] = daily
    # data["hijri"] = pray_today.hijri
    # build context
    # context = {'info' : info}
    return render(
        request,
        "home.html",
        {
            "page": {"title": _("home"), "icon": HOME_ICON, "index": HOME_ID},
            "data": data,
            # "page_index": HOME_ID,
        },
    )


def callus(request: HttpRequest):
    # form = CallUsForm()

    if request.POST:
        name = request.POST.get("your_name")
        email = request.POST.get("your_email")
        message = request.POST.get("your_message")
        if name and email and message:
            CallUs.objects.create(message=message, email=email, name=name)
            messages.add_message(request, messages.SUCCESS, _("message send successfully"))

        else:
            messages.add_message(request, messages.ERROR, _("data is not valid"))

    phone_numbers = PhoneNumbers.objects.all()
    emails = Email.objects.all()
    return render(
        request,
        "callus.html",
        {
            "page": {"title": _("call us"), "icon": CALLUS_ICON, "index": CALLUS_ID},
            # "form": form,
            "page_index": CALLUS_ID,
            "mobiles": [el for el in phone_numbers if el.phone_number_type == "mobile"],
            "telephons": [el for el in phone_numbers if el.phone_number_type == "telephon"],
            "faxs": [el for el in phone_numbers if el.phone_number_type == "fax"],
            "emails": emails,
        },
    )


def books(request):
    # book ,artical

    # books = Book.objects.filter(status=STATUS_PUBLISHED, type="book").all()
    # return render(
    #     request,
    #     "books.html",
    #     {
    #         "page": {"title": _("book_list"), "icon": BOOKS_ICON, "index": BOOKS_ID},
    #         "books": books,
    #         "type": "book",
    #     },
    # )
    return base_books_view(request, type="book")


def articals(request):

    # articals = Book.objects.filter(status=STATUS_PUBLISHED, type="artical").all()

    # return render(
    #     request,
    #     "books.html",
    #     {
    #         "page": {"title": _("book_list"), "icon": BOOKS_ICON, "index": BOOKS_ID},
    #         "books": articals,
    #         "type": "artical",
    #     },
    # )

    return base_books_view(request, type="artical")


def base_books_view(request, type="book"):
    articals = Book.objects.filter(status=STATUS_PUBLISHED, type="artical").all()
    books = Book.objects.filter(status=STATUS_PUBLISHED, type="book").all()

    return render(
        request,
        "books.html",
        {
            "page": {"title": _("books and articles"), "icon": BOOKS_ICON, "index": BOOKS_ID},
            "articals": articals,
            "books": books,
            "type": type,
        },
    )


def book_by_pk(request, pk: int):
    book = Book.objects.get(id=pk)
    search = BookSeach.objects.filter(book_id=pk)
    return render(
        request,
        "book.html",
        {
            "page": {"title": f"{_('book')} {book.title }", "icon": BOOKS_ICON, "index": BOOKS_ID},
            "book": book,
            'search_result': search,
        },
    )


# def list_media_view(request, media, url="", page_title="", main_header_title="", content_header="", url_youtube="", not_found=False):
#     return render(
#         request,
#         "list_media_view.html",
#         {
#             "page": {"title": page_title},
#             "main_header_title": main_header_title,
#             "content_header": content_header,
#             "url": url,
#             "url_youtube": url_youtube,
#             "media": media,
#             "not_found": not_found,
#         },
#     )


def render_general_media_show(
    request, media, page_title, main_header_title, page_index, icon, content_header="", url_youtube="", url="", not_found=False
):
    # print("url_youtube", url_youtube)
    return render(
        request,
        "media_show.html",
        {
            "page": {"title": page_title, "icon": icon, "index": page_index},
            "main_header_title": main_header_title,
            "content_header": content_header,
            "url": url,
            "url_youtube": youtube_url(url_youtube),
            "media": media,
            "not_found": not_found,
        },
    )


def quran(request):
    return quran_sura(request)


def quran_sura(request, sura_id=None):

    suras = Sura.objects.only("name").all()

    sura = None
    quran_text = None
    if sura_id:
        sura = suras.get(id=sura_id)

    if not sura:
        sura = suras.first()

    quran_text = sura.all_ayas()

    return render(
        request,
        "quran.html",
        {
            "page": {"title": _("quran"), "icon": QURAN_ICON, "index": QURAN_ID},
            "suras": suras,
            "page_index": QURAN_ID,
            "suras": suras,
            "sura": sura,
            "quran_text": quran_text,
        },
    )


def quran_media(request, sura_number):
    youtube = ""
    url = ""
    media = ""
    main_header_title = ""
    page_title = ""
    sura = Sura.objects.get(id=sura_number)
    if "video" in request.path:
        media = "video"
        youtube = ""
        url = ""
        ayat_tafsir = AyatTafsirVideo.objects.filter(sura=sura_number, status=STATUS_PUBLISHED).order_by("sura", "aya_start").all()
    elif "audio" in request.path:
        media = "audio"
        ayat_tafsir = AyatTafsirAudio.objects.filter(sura=sura_number, status=STATUS_PUBLISHED).order_by("sura", "aya_start").all()

    elif "telawa" in request.path:
        media = "telawa"
        ayat_tafsir = AyatTelawa.objects.filter(sura=sura_number, status=STATUS_PUBLISHED).order_by("sura", "aya_start").all()

    elif "read" in request.path:
        media = "read"

    content_header = f" {_('sura')} {sura.name}  {_('(هذا المحتوى غير متوفر حالياً)')} "
    res = []
    ayatList = Ayat.objects.filter(sura=sura_number).all()
    for aya_t in ayat_tafsir:
        aya_start = f"{_('from')} {_('aya')}  {aya_t.aya_start.count} " if aya_t.aya_start else ""
        aya_end = f"{_('to')} {_('aya')}  {aya_t.aya_end.count} " if aya_t.aya_end else ""

        part_ayat_list = ayatList.filter(count__lte=aya_t.aya_end.count, count__gte=aya_t.aya_start.count).only("text")
        ayat_text = from_ayat_to_text(part_ayat_list, sura_number)

        res.append(
            {
                "title": f"{aya_start} {aya_end}",
                "id": aya_t.id,
                "file": aya_t.sound_tafsir if media == "audio" else aya_t.telawa if media == "telawa" else aya_t.video_tafsir,
                "video_url": youtube_url(aya_t.video_url) if media == "video" else None,
                "text": SafeString(ayat_text),
            }
        )

    paginator = Paginator(res, items_per_page)  # Show 14.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    med_title = _("sound_tafsir" if media == "audio" else "video_tafsir" if media == "video" else "telawa" if media == "telawa" else "read")

    return render(
        request,
        "list_media_view.html",
        {
            "page": {
                "title": f"{_('quran')} / {_('sura')} {sura.name} / {med_title} ",
                "icon": QURAN_ICON,
                "index": QURAN_ID,
            },
            "title": SafeString(
                get_title_url(_("quran"), "quran")
                + get_title_url(f" / {_('sura')} {sura.name}", "quran_sura", {"sura_id": sura.id})
                + f" / {med_title} "
            ),
            "page_obj": page_obj,
            "content_header": content_header,
            "media": media,
            "page_index": QURAN_ID,
        },
    )


def quran_media_read(request, sura_number):
    media = "read"
    med_title = _("Readed Tafsir")
    sura = Sura.objects.get(id=sura_number)
    content_header = f" {_('sura')} {sura.name}  {_('(هذا المحتوى غير متوفر حالياً)')} "
    return render(
        request,
        "list_media_view.html",
        {
            "page": {
                "title": f"{_('quran')} / {_('sura')} {sura.name} / {med_title} ",
                "icon": QURAN_ICON,
                "index": QURAN_ID,
            },
            "title": SafeString(
                get_title_url(_("quran"), "quran")
                + get_title_url(f" / {_('sura')} {sura.name}", "quran_sura", {"sura_id": sura.id})
                + f" / {med_title} "
            ),
            "content_header": content_header,
            "media": media,
            "page_index": QURAN_ID,
        },
    )


def quran_media_video_part(request, tafsir_id):
    tafsir = AyatTafsirVideo.objects.filter(
        status=STATUS_PUBLISHED,
        id=tafsir_id,
    ).first()
    media = ""

    if "video" in request.path:
        media = "video"

    elif "audio" in request.path:
        media = "audio"

    elif "telawa" in request.path:
        media = "telawa"
    med_title = _("sound_tafsir" if media == "audio" else "video_tafsir" if media == "video" else "telawa")
    # med_url = _("quran_media_audio" if media == "audio" else "video_tafsir" if media == "video" else "telawa")
    if tafsir and tafsir.video_tafsir and tafsir.aya_start and tafsir.aya_end:
        part_ayat_list = (
            Ayat.objects.filter(count__lte=tafsir.aya_end.count, count__gte=tafsir.aya_start.count, sura=tafsir.sura).only("text").all()
        )
        ayat_text = from_ayat_to_text(part_ayat_list, tafsir.sura.number)
        return render_general_media_show(
            request,
            "video",
            url=tafsir.video_tafsir.url,
            page_title=f"{_('video_tafsir')}  ",
            # main_header_title=f"{_('video_tafsir')} / {_('AyatTafsir')} ",
            main_header_title=SafeString(
                get_title_url(_("quran"), "quran")
                + get_title_url(f" / {_('sura')} {tafsir.sura.name}", "quran_sura", {"sura_id": tafsir.sura.id})
                + " / "
                + get_title_url(med_title, f"quran_media_{media}", {"sura_number": tafsir.sura.id})
            ),
            content_header=SafeString(ayat_text),
            url_youtube=youtube_url(tafsir.video_url),
            page_index=QURAN_ID,
            icon=QURAN_ICON,
        )
    else:

        return render_general_media_show(
            request,
            "video",
            page_index=QURAN_ID,
            page_title=f"{_('video_tafsir')} ",
            main_header_title=f"{_('video_tafsir')} / {_('AyatTafsir')} ",
            # f"  {_('from')} : {_('aya')} {tafsir.aya_start.count} {_('to')} : {tafsir.aya_end.count}
            content_header=f"{_('(هذا المحتوى غير متوفر حالياً)')}",
            not_found=True,
            icon=QURAN_ICON,
        )


def saheh(request):
    # al_saheh_books = BookInAlSaheh.objects.all()
    # return render(
    #     request,
    #     "saheh.html",
    #     {
    #         "page": {
    #             "title": _("AlHadith"),
    #             "icon": HADITH_ICON,
    #             "index": HADITH_ID,
    #         },
    #         "title": _("AlHadith/AlSaheh"),
    #         "al_saheh_books": al_saheh_books,
    #     },
    # )

    # return saheh_book(request, id)

    # al_saheh_books = BookInAlSaheh.objects.all()
    # #

    # mybook = al_saheh_books.first()
    # book_chapters = ChapterInAlSaheh.objects.filter(book=mybook.id)
    # #
    # mychapter = book_chapters.first()
    # all_hadith_in_chapter = None
    # if mychapter:
    #     all_hadith_in_chapter = Hadith.objects.filter(book=mybook.id, chapter=mychapter.id).all()

    # return render(
    #     request,
    #     "saheh.html",
    #     {
    #         "page": {
    #             "title": _("AlHadith"),
    #             "icon": HADITH_ICON,
    #             "index": HADITH_ID,
    #         },
    #         "title": _("AlHadith/AlSaheh"),
    #         "al_saheh_books": al_saheh_books,
    #         "page_index": HADITH_ID,
    #         "mybook": mybook,
    #         "book_chapters": book_chapters,
    #         "chapter_hadiths": all_hadith_in_chapter,
    #         "mychapter": mychapter,
    #     },
    # )

    # book_id = BookInAlSaheh.objects.only("id").first().id
    # mychapter = ChapterInAlSaheh.objects.only("id").filter(book_id=book_id).last()
    # print(f"book {book_id}")
    # print(f"mychapter {mychapter}")
    return saheh_chapter(
        request,
        1
        # mychapter.id if mychapter else None
        # 2,
    )


def saheh_book(request, book_id):
    # al_saheh_books = BookInAlSaheh.objects.all()
    # book_chapters = ChapterInAlSaheh.objects.filter(book=book_id)
    # mybook = BookInAlSaheh.objects.filter(id=book_id).first()

    # return render(
    #     request,
    #     "saheh.html",
    #     {
    #         "page": {
    #             "title": _("AlHadith"),
    #             "icon": HADITH_ICON,
    #             "index": HADITH_ID,
    #         },
    #         "title": _("AlHadith/AlSaheh"),
    #         "al_saheh_books": al_saheh_books,
    #         "page_index": HADITH_ID,
    #         "mybook": mybook,
    #         "book_chapters": book_chapters,
    #     },
    # )
    mybook = BookInAlSaheh.objects.only("id").filter(id=book_id, active_flag = True).first()
    chapter_id = ChapterInAlSaheh.objects.only("id").filter(book_id=mybook.id).first().id
    return saheh_chapter(request, chapter_id)


def saheh_chapter(request, chapter_id):
    al_saheh_books = BookInAlSaheh.objects.filter(active_flag = True).all().order_by("order_by")
    intro_book = al_saheh_books.first().id
    # al_saheh_books = [intro_book].extend(al_saheh_books[:-1])

    al_saheh_books = al_saheh_books[0 : len(al_saheh_books) - 1]
    # al_saheh_books.insert(0, intro_book)

    mychapter = None
    mybook = None
    book_chapters = None
    all_hadith_in_chapter = None
    if chapter_id ==1 :
        mychapter = ChapterInAlSaheh.objects.filter(book=intro_book).first()
    else:
        mychapter = ChapterInAlSaheh.objects.filter(id=chapter_id).first()
    #
    mybook = mychapter.book
    book_chapters = ChapterInAlSaheh.objects.filter(book=mychapter.book.id)
    #
    all_hadith_in_chapter = Hadith.objects.filter(book=mychapter.book.id, chapter=mychapter.id).all()

    return render(
        request,
        "saheh.html",
        {
            "page": {
                "title": _("AlHadith"),
                "icon": HADITH_ICON,
                "index": HADITH_ID,
            },
            "title": _("AlHadith/AlSaheh"),
            "al_saheh_books": al_saheh_books,
            "page_index": HADITH_ID,
            "mybook": mybook,
            "book_chapters": book_chapters,
            "chapter_hadiths": all_hadith_in_chapter,
            "mychapter": mychapter,
        },
    )


def saheh_media(request: HttpRequest, hadith_number):

    # book_number
    media = ""
    url = ""
    url_youtube = ""
    had_text = ""
    tafsir = TafsirHadithInAlSaheh.objects.filter(hadith=hadith_number, status=STATUS_PUBLISHED).last()
    if tafsir and (("video" in request.path and tafsir.video_tafsir) or ("audio" in request.path and tafsir.audio_tafsir)):
        if "video" in request.path:
            media = "video"
            url = tafsir.video_tafsir.url
            url_youtube = youtube_url(tafsir.video_url)
        elif "audio" in request.path:
            media = "audio"
            url = tafsir.audio_tafsir.url
    # print("url_youtube", url_youtube)
    if tafsir and media != "":

        main_header_title = ""
        AlHadith = get_title_url(f"{_('AlHadith')}", "saheh")
        # AlHadith = get_title_url(f"{_('AlHadith')} ({_('AlSaheh')}) ", "saheh", {})
        book = " / " + get_title_url(str(tafsir.book.name), "saheh_book", {"book_id": tafsir.book.id})
        chapter = " / " + get_title_url(f" { tafsir.chapter.name} ", "saheh_chapter", {"chapter_id": tafsir.chapter.id})
        # chapter = "/ {_('chapter') } {str(tafsir.chapter.name)} "
        main_header_title = AlHadith + book + chapter
        # return render(request, "saheh_media1.html", {"page": {"title": title}, "tafsir": tafsir, "media": media})
        # return render(request, "media_show.html", {"page": {"title": title}, "url":tafsir., "media": media})
        had_text = tafsir.hadith.text

        return render_general_media_show(
            request,
            media,
            url=url,
            page_title=f"{_('AlHadith/AlSaheh')}",
            main_header_title=SafeString(main_header_title),
            content_header=f" {had_text}",
            url_youtube=url_youtube,
            not_found=False,
            page_index=HADITH_ID,
            icon=HADITH_ICON,
        )

    else:
        return render_general_media_show(
            request,
            media,
            page_title=f"{_('AlHadith/AlSaheh')}",
            main_header_title=f"{_('AlHadith/AlSaheh')} / {_('hadith_number')} : {hadith_number} ",
            content_header=f"{_('number') } {_('hadith') } : {hadith_number}   {_('(هذا المحتوى غير متوفر حالياً)')}  ",
            not_found=True,
            page_index=HADITH_ID,
            icon=HADITH_ICON,
        )


def saheh_media_read(request, hadith_number):
    hadith = Hadith.objects.get(id=hadith_number)
    media = "read"
    AlHadith = get_title_url(f"{_('AlHadith')} ({_('الصحيح')}) ", "saheh")
    book = " / " + get_title_url(str(hadith.book.name), "saheh_book", {"book_id": hadith.book.id})
    chapter = " / " + get_title_url(f" { hadith.chapter.name} ", "saheh_chapter", {"chapter_id": hadith.chapter.id})
    return render_general_media_show(
        request,
        media,
        page_title=f"{_('AlHadith/AlSaheh')}",
        main_header_title=SafeString(AlHadith + book + chapter + " / " + _("Readed Tafsir")),
        content_header=f"{_('number') } {_('hadith') } : {hadith_number}   {_('(هذا المحتوى غير متوفر حالياً)')}  ",
        not_found=True,
        page_index=HADITH_ID,
        icon=HADITH_ICON,
    )


def fatwa(request):

    fatwa_list = Fatwa.objects.filter(status=STATUS_PUBLISHED).all()

    # res = urls.reverse("base:fatwa_media", args=[fatwa_list[0].id])

    # lista = []
    # for item in fatwa_list:
    #     lista.append()

    # paginator = Paginator(fatwa_list, 14)  # Show 14.
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)

    # return render(
    #     request,
    #     "list_media_view.html",
    #     {"page": {"title": f"{_('fatwas')}"}, "page_obj": page_obj},
    # )

    return render(
        request,
        "fatwa.html",
        {
            "page": {
                "title": _("Fatwas"),
                "icon": FATWA_ICON,
                "index": FATWA_ID,
            },
            # "page_obj": page_obj,
            "fatwa": fatwa_list,
            # "content_header": content_header,
            "media": "audio",
        },
    )


def fatwa_media(request, fatwa_id):
    fatwa = Fatwa.objects.get(id=fatwa_id)
    if fatwa.status == "p":

        return render_general_media_show(
            request,
            media="audio",
            content_header="",
            main_header_title=SafeString(get_title_url(_("Fatwas"), "fatwa") + f' / {_("title")}'),
            page_title="",
            url=fatwa.file.url,
            # url_youtube=fatwa.video_url,
            not_found=False,
            page_index=FATWA_ID,
            icon=FATWA_ICON,
        )
    else:
        return render_general_media_show(
            request,
            media="audio",
            content_header="",
            main_header_title=f"{_('(هذا المحتوى غير متوفر حالياً)')}",
            page_title="",
            not_found=True,
            page_index=FATWA_ID,
            icon=FATWA_ICON,
        )


# start session


def sessions(request):

    # return sessions_type(request, None)
    type = "quran"
    cat_id = SessionsCategory.objects.only("id").filter(type=type, active_flag=True).first().id
    return sessions_category(request, type, cat_id)

def sessions_quran(request):

    # return sessions_type(request, None)
    type = "quran"
    cat_id = SessionsCategory.objects.only("id").filter(type=type, active_flag=True).first().id
    return sessions_cat_quran(request, type, cat_id)

def sessions_pillars(request):

    # return sessions_type(request, None)
    type = "pillars"
    cat_id = SessionsCategory.objects.only("id").filter(type=type, active_flag=True).first().id
    return sessions_cat_pillars(request, type, cat_id)


def sessions_hadith(request):

    # return sessions_type(request, None)
    type = "hadith"
    cat_id = SessionsCategory.objects.only("id").filter(type=type, active_flag=True).first().id
    return sessions_cat_hadith(request, type, cat_id)

def sessions_othersciences(request):

    # return sessions_type(request, None)
    type = "OtherScience"
    cat_id = SessionsCategory.objects.only("id").filter(type=type, active_flag=True).first().id
    return sessions_cat_othersciences(request, type, cat_id)

def sessions_type(request, type):
    # page_obj = None
    # sessions_list = None
    type = type if type else "quran"

    # # sessions_list = Sessions.objects.filter(type=type, status=STATUS_PUBLISHED).order_by("file__folder", "title").all()
    # # values_list('sound_tafsir', flat=True)
    # sessions_category_list = SessionsCategory.objects.filter(type=type, active_flag=True).order_by("name", "type").all()

    # # paginator = Paginator(sessions_list, items_per_page)  # Show 25   per page.

    # # page_number = request.GET.get("page")
    # # page_obj = paginator.get_page(page_number)

    # return render(
    #     request,
    #     "sessions.html",
    #     {
    #         "page": {
    #             "main_header_title": f"{_('Sessions')}",
    #             "title": f"{_('Sessions')}",
    #             "sub_title": f'  {_("Sessions")} ',
    #             "icon": SESSION_ICON,
    #             "index": SESSION_ID,
    #         },
    #         "page_obj": page_obj,
    #         # "data": sessions_list,
    #         "categorys": sessions_category_list,
    #         "session_type_list": [{"type": item[0], "name": item[1]} for item in SESSIONS_TYPE],
    #         "type": type,
    #     },
    # )
    name_category = SessionsCategory.objects.filter(type=type, active_flag=True).only("id").order_by("name", "type").first().id
    return sessions_category(request, type, name_category)


def sessions_category(request, type, category):

    sessions_category_list = SessionsCategory.objects.filter(type=type, active_flag=True).all()
    category = sessions_category_list.filter(id=category).first()
    page_obj = None
    sessions_list = None
    if type=='quran':
        SESSION_ID = 11
    elif type=='hadith':
        SESSION_ID = 12
    elif type=='OtherScience':
        SESSION_ID = 13
    else:
        SESSION_ID = 14

    #sessions_list = Sessions.objects.filter(category=category, type=type, status=STATUS_PUBLISHED).order_by("file__folder", "title").all()
    sessions_list = Sessions.objects.filter(category=category, type=type, status=STATUS_PUBLISHED).order_by("order_by").all()
    # values_list('sound_tafsir', flat=True)
    paginator = Paginator(sessions_list, items_per_page)  # Show 25   per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "sessions.html",
        {
            "page": {
                "main_header_title": f"{_('Sessions')}",
                "title": f"{_('Sessions')}",
                "sub_title": f'  {_("Sessions")} ',
                "icon": SESSION_ICON,
                "index": SESSION_ID,
            },
            "page_obj": page_obj,
            "data": sessions_list,
            "session_type_list": [{"type": item[0], "name": item[1]} for item in SESSIONS_TYPE],
            "type": type,
            "category": category,
            "categorys": sessions_category_list,
        },
    )

def sessions_cat_hadith(request, type, category):

    sessions_category_list = SessionsCategory.objects.filter(type=type, active_flag=True).all()
    category = sessions_category_list.filter(id=category).first()
    page_obj = None
    sessions_list = None

    #sessions_list = Sessions.objects.filter(category=category, type=type, status=STATUS_PUBLISHED).order_by("file__folder", "title").all()
    sessions_list = Sessions.objects.filter(category=category, type=type, status=STATUS_PUBLISHED).order_by("order_by").all()
    #return sessions_list
    # values_list('sound_tafsir', flat=True)
    paginator = Paginator(sessions_list, items_per_page)  # Show 25   per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "sessions_hadith.html",
        {
            "page": {
                "main_header_title": f"{_('Sessions')}",
                "title": f"{_('Sessions')}",
                "sub_title": f'  {_("Sessions")} ',
                "icon": SESSION_ICON,
                "index": MAJALIS_HADITH_ID,
            },
            "page_obj": page_obj,
            "data": sessions_list,
            "session_type_list": [{"type": item[0], "name": item[1]} for item in SESSIONS_TYPE],
            "type": type,
            "category": category,
            "categorys": sessions_category_list,
        },
    )

def sessions_cat_quran(request, type, category):

    sessions_category_list = SessionsCategory.objects.filter(type=type, active_flag=True).all()
    category = sessions_category_list.filter(id=category).first()
    page_obj = None
    sessions_list = None

    #sessions_list = Sessions.objects.filter(category=category, type=type, status=STATUS_PUBLISHED).order_by("file__folder", "title").all()
    sessions_list = Sessions.objects.filter(category=category, type=type, status=STATUS_PUBLISHED).order_by("order_by").all()
    #return sessions_list
    # values_list('sound_tafsir', flat=True)
    paginator = Paginator(sessions_list, items_per_page)  # Show 25   per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "sessions_quran.html",
        {
            "page": {
                "main_header_title": f"{_('Sessions')}",
                "title": f"{_('Sessions')}",
                "sub_title": f'  {_("Sessions")} ',
                "icon": SESSION_ICON,
                "index": MAJALIS_QURAN_ID,
            },
            "page_obj": page_obj,
            "data": sessions_list,
            "session_type_list": [{"type": item[0], "name": item[1]} for item in SESSIONS_TYPE],
            "type": type,
            "category": category,
            "categorys": sessions_category_list,
        },
    )

def sessions_cat_pillars(request, type, category):

    sessions_category_list = SessionsCategory.objects.filter(type=type, active_flag=True).all()
    category = sessions_category_list.filter(id=category).first()
    page_obj = None
    sessions_list = None

    #sessions_list = Sessions.objects.filter(category=category, type=type, status=STATUS_PUBLISHED).order_by("file__folder", "title").all()
    sessions_list = Sessions.objects.filter(category=category, type=type, status=STATUS_PUBLISHED).order_by("order_by").all()
    #return sessions_list
    # values_list('sound_tafsir', flat=True)
    paginator = Paginator(sessions_list, items_per_page)  # Show 25   per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "sessions_pillars.html",
        {
            "page": {
                "main_header_title": f"{_('Sessions')}",
                "title": f"{_('Sessions')}",
                "sub_title": f'  {_("Sessions")} ',
                "icon": SESSION_ICON,
                "index": PILLARS_ID,
            },
            "page_obj": page_obj,
            "data": sessions_list,
            "session_type_list": [{"type": item[0], "name": item[1]} for item in SESSIONS_TYPE],
            "type": type,
            "category": category,
            "categorys": sessions_category_list,
        },
    )
def sessions_cat_othersciences(request, type, category):

    sessions_category_list = SessionsCategory.objects.filter(type=type, active_flag=True).all()
    category = sessions_category_list.filter(id=category).first()
    page_obj = None
    sessions_list = None

    #sessions_list = Sessions.objects.filter(category=category, type=type, status=STATUS_PUBLISHED).order_by("file__folder", "title").all()
    sessions_list = Sessions.objects.filter(category=category, type=type, status=STATUS_PUBLISHED).order_by("order_by").all()
    #return sessions_list
    # values_list('sound_tafsir', flat=True)
    paginator = Paginator(sessions_list, items_per_page)  # Show 25   per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "sessions_other_sciences.html",
        {
            "page": {
                "main_header_title": f"{_('Sessions')}",
                "title": f"{_('Sessions')}",
                "sub_title": f'  {_("Sessions")} ',
                "icon": SESSION_ICON,
                "index": MAJALIS_OTHER_SCIENCE_ID,
            },
            "page_obj": page_obj,
            "data": sessions_list,
            "session_type_list": [{"type": item[0], "name": item[1]} for item in SESSIONS_TYPE],
            "type": type,
            "category": category,
            "categorys": sessions_category_list,
        },
    )

def session_media(request, session_id):
    session = Sessions.objects.get(id=session_id)

    return render_general_media_show(
        request,
        media="video",
        content_header="",
        main_header_title=SafeString(
            get_title_url(_("Sessions"), "sessions")
            + " / "
            + get_title_url(_(session.type), "sessions_type", {"type": session.type})
            + f" / {session.title}"
        ),
        page_title=f'{_("Sessions")} / {_(session.type)}',
        url=session.file.url,
        url_youtube=youtube_url(session.video_url),
        not_found=False,
        page_index=SESSION_ID,
        icon=SESSION_ID,
    )


# def quran_tartil_audio(request):

#     tartil_audio_list = AyatTafsir.objects.filter(status=STATUS_PUBLISHED).all()
#     # values_list('telawa', flat=True)

#     # paginator = Paginator(tartil_audio_list, 1)  # Show 25   per page.

#     # page_number = request.GET.get("page")
#     # page_obj = paginator.get_page(page_number)
#     page_obj = tartil_audio_list

#     # title = f"{_('quran')}/{_('telawa')}/{sura}"

#     return render(
#         request,
#         "list_media_view.html",
#         {"page": {"title": f"{_('AyatTafsir')}"}, "page_obj": page_obj},
#     )


# def quran_tafsir_audio(request):
#
#     tafsir_audio_list = AyatTafsir.objects.filter(status=STATUS_PUBLISHED).all()
#     # values_list('sound_tafsir', flat=True)
#     paginator = Paginator(tafsir_audio_list, 1)  # Show 25   per page.

#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         "list_media_view.html",
#         {"page": {"title": f"{_('telawa')}"}, "page_obj": page_obj},
#     )


def other_science(request):

    return other_science_subject(request, None)

def other_science_subject(request, subject_id):

    subject = OtherScienceSubject.objects.filter(status=STATUS_PUBLISHED)

    subject_video = subject.filter(file_type="video").all()
    subject_audio = subject.filter(file_type="audio").all()
    OtherScience_data = None
    my_subject = None
    _my_subject_link = ""
    if subject_id:
        my_subject = OtherScienceSubject.objects.get(id=subject_id)
    else:
        my_subject = OtherScienceSubject.objects.first()

    OtherScience_data = OtherScience.objects.filter(subject_id=my_subject.id, status=STATUS_PUBLISHED).all()
    _my_subject_link = get_title_url(f"/  {my_subject.subjects} ", "other_science_subject", {"subject_id": my_subject.id})
    return render(
        request,
        "other_science.html",
        {
            "page": {
                "title": f"{_('OtherScience')}",
                "main_header_title": SafeString(get_title_url(f"{_('OtherScience')} ", "other_science") + _my_subject_link),
                "sub_title_audio": f'{_("other science audio")}',
                "sub_title_video": f'{_("other science video")}',
                "icon": OTHER_SCIENCE_ICON,
                "index": OTHER_SCIENCE_ID,
            },
            "subject_video": subject_video,
            "subject_audio": subject_audio,
            "data": OtherScience_data,
            "subject": my_subject,
            "page_index": OTHER_SCIENCE_ID,
        },
    )


def other_science_subject_video(request, other_science_id):
    science = OtherScience.objects.get(id=other_science_id)

    _my_subject_link = ""
    if other_science_id:
        # my_subject = OtherScienceSubject.objects.get(id=science.subject.id)

        # _my_subject_link = get_title_url(f"/  {my_subject.subjects} ", "other_science_subject", {"subject_id": my_subject.id})
        _my_subject_link = get_title_url(f"{science.subject.subjects} ", "other_science_subject", {"subject_id": science.subject.id})

    return render_general_media_show(
        request,
        media="video",
        content_header="",
        main_header_title=SafeString(get_title_url(_("OtherScience"), "other_science") + f"/  {_my_subject_link} / {science.title}  "),
        page_title=f"{_('OtherScience')} /  {science.title}  ",
        url=science.file.url,
        url_youtube=youtube_url(science.video_url),
        page_index=OTHER_SCIENCE_VIDEO_ID,
        icon=OTHER_SCIENCE_ICON,
    )

def other_science_audio(request):

    return other_science_audio_subject(request, None)

def other_science_audio_subject(request, subject_id):

    subject = OtherScienceSubject.objects.filter(status=STATUS_PUBLISHED).order_by('order')

    subject_video = subject.filter(file_type="video").all()
    subject_audio = subject.filter(file_type="audio").all()
    OtherScience_data = None
    my_subject = None
    _my_subject_link = ""
    if subject_id:
        my_subject = OtherScienceSubject.objects.get(id=subject_id)
    else:
        my_subject = OtherScienceSubject.objects.first()


    #exit(OTHER_SCIENCE_AUDIO_ID)

    OtherScience_data = OtherScience.objects.filter(subject_id=my_subject.id, status=STATUS_PUBLISHED).all().order_by("order_by")
    _my_subject_link = get_title_url(f"/  {my_subject.subjects} ", "other_science_audio_subject", {"subject_id": my_subject.id})
    return render(
        request,
        "other_science_audio.html",
        {
            "page": {
                "title": f"{_('OtherScience')}",
                "main_header_title": SafeString(get_title_url(f"{_('OtherScience')} ", "other_science_audio") + _my_subject_link),
                "sub_title_audio": f'{_("other science audio")}',
                "sub_title_video": f'{_("other science video")}',
                "icon": OTHER_SCIENCE_ICON,
                "index": OTHER_SCIENCE_AUDIO_ID,
            },
            "subject_video": subject_video,
            "subject_audio": subject_audio,
            "data": OtherScience_data,
            "subject": my_subject,
            "page_index": OTHER_SCIENCE_AUDIO_ID,
        },
    )

def other_science_video(request):

    return other_science_video_subject(request, 16)

def other_science_video_subject(request, subject_id):

    subject = OtherScienceSubject.objects.filter(status=STATUS_PUBLISHED).order_by('order')

    subject_video = subject.filter(file_type="video").all()
    #subject_audio = subject.filter(file_type="audio").all()
    OtherScience_data = None
    my_subject = None
    _my_subject_link = ""
    if subject_id:
        my_subject = OtherScienceSubject.objects.get(id=subject_id)
    else:
        my_subject = OtherScienceSubject.objects.first()

    OtherScience_data = OtherScience.objects.filter(subject_id=my_subject.id, status=STATUS_PUBLISHED).all().order_by("order_by")
    _my_subject_link = get_title_url(f"/  {my_subject.subjects} ", "other_science_video_subject", {"subject_id": my_subject.id})
    return render(
        request,
        "other_science_video.html",
        {
            "page": {
                "title": f"{_('OtherScience')}",
                "main_header_title": SafeString(get_title_url(f"{_('OtherScience')} ", "other_science_video") + _my_subject_link),
                "sub_title_audio": f'{_("other science audio")}',
                "sub_title_video": f'{_("other science video")}',
                "icon": OTHER_SCIENCE_ICON,
                "index": OTHER_SCIENCE_VIDEO_ID,
            },
            "subject_video": subject_video,
            #"subject_audio": subject_audio,
            "data": OtherScience_data,
            "subject": my_subject,
            "page_index": OTHER_SCIENCE_VIDEO_ID,
        },
    )

def read_quran(request):

    return read_quran_page(
        request,
    )


def read_quran_page(request, page=None):

    return render(
        request,
        "read_quran.html",
        {
            "page": {
                "title": f"{_('read quran')}",
                "icon": QURAN_ICON,
                "index": QURAN_ID,
            },
            "title": f"{_('electonic quran')}",
            "page_number": page,
        },
    )


def about_us(request):
    general = General_information.objects.first()

    return render(
        request,
        "about_us.html",
        {
            "page": {
                "title": f"{_('about us')}",
                "icon": HOME_ICON,
                "index": HOME_ID,
            },
            "mousa_img": general.mousa_img.url if general and general.mousa_img else None,
            "sheikh_img": general.sheikh_img.url if general and general.sheikh_img else None,
        },
    )


def related_sites(request):
    related = RelatedSites.objects.all()
    return render(
        request,
        "related_site.html",
        {
            "page": {
                "title": f"{_('related sites')}",
                "icon": HOME_ICON,
                "index": HOME_ID,
            },
            "sites": related,
        },
    )


def policy(request):

    general = General_information.objects.all()
    if len(general):
        policy = general[0].privacy_policy
    return render(
        request,
        "policy.html",
        {
            "page": {
                "title": f"{_('related sites')}",
                "icon": HOME_ICON,
                "index": HOME_ID,
            },
            "policy": policy,
        },
    )


# def prayer_city(request, city: str):
#     pray_obj = get_pray(city=city)
#     print(pray_obj)
#     if not pray_obj:
#         return JsonResponse({})

#     pray_data = {}
#     if pray_obj.Fajr:

#         pray_data["Fajr"] = format_time(pray_obj.Fajr)
#     if pray_obj.Sunrise:
#         pray_data["Sunrise"] = format_time(pray_obj.Sunrise)
#     if pray_obj.Dhuhr:
#         pray_data["Dhuhr"] = format_time(pray_obj.Dhuhr)
#     if pray_obj.Asr:
#         pray_data["Asr"] = format_time(pray_obj.Asr)
#     if pray_obj.Maghrib:
#         pray_data["Maghrib"] = format_time(pray_obj.Maghrib)
#     if pray_obj.Isha:
#         pray_data["Isha"] = format_time(pray_obj.Isha)

#     return JsonResponse(pray_data)


class SearchView(ListView):
    template_name = "search_view.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["quran"] = Sura.objects.all()
        context["ayat_tafsir"] = AyatTafsirVideo.objects.filter(status=STATUS_PUBLISHED).all()
        context["books"] = Book.objects.filter(status=STATUS_PUBLISHED, type="book").all()
        context["hadith_books"] = BookInAlSaheh.objects.all()
        context["othersciencesubjects"] = OtherScienceSubject.objects.filter(status=STATUS_PUBLISHED).all()
        context["query"] = self.request.GET.get("q") or self.request.GET.get("mainq")
        context["page"] = {
            "title": f"{_('search')}",
            "icon": SEARCH_ICON,
            "index": HOME_ID,
        }

        return context

    def get_queryset(self):
        request = self.request
        query = request.GET
        sentence = query.get("q")
        sura = query.get("quran")
        hadith_book_id = query.get("hadith_book_id")
        book = query.get("book")

        qurancheck = query.get("qurancheck")
        hadithcheck = query.get("hadithcheck")
        bookcheck = query.get("bookcheck")
        othersciencecheck = query.get("othersciencecheck")
        fatwacheck = query.get("fatwacheck")

        # if searching from main search bar will search in all topics
        if query.get("mainq"):
            sentence = query.get("mainq")
            qurancheck = hadithcheck = bookcheck = othersciencecheck = fatwacheck = "on"

        if sentence:
            # query for quran
            if qurancheck:
                if sura:
                    quran_results = Ayat.objects.filter(text_without_tashkil__icontains=sentence, sura_id=sura)
                else:
                    quran_results = Ayat.objects.filter(text_without_tashkil__icontains=sentence)
            else:
                quran_results = []

            # query for hadith
            if hadithcheck:
                if hadith_book_id:

                    hadith_results = Hadith.objects.filter(text_without_tashkil__icontains=sentence, id=hadith_book_id)
                else:
                    hadith_results = Hadith.objects.filter(text_without_tashkil__icontains=sentence)
            else:
                hadith_results = []

            # query for books
            if bookcheck:
                if book:
                    book_results = Book.objects.filter(title__icontains=sentence, id=book)
                    book_content_results = BookSeach.objects.filter(book=book, key__icontains=sentence).all()
                else:
                    book_results = Book.objects.filter(title__icontains=sentence)
                    book_content_results = BookSeach.objects.filter(key__icontains=sentence).all()
            else:
                book_results = []
                book_content_results = []

            # query for other sciences
            if othersciencecheck:
                otherscience_results = OtherScience.objects.filter(status=STATUS_PUBLISHED).filter(title__icontains=sentence)
            else:
                otherscience_results = []

            # query for fatwa
            if fatwacheck:
                fatwa_results = Fatwa.objects.filter(status=STATUS_PUBLISHED).filter(title__icontains=sentence)
            else:
                fatwa_results = []
            # print("book_content_results", book_content_results)
            all_query = {
                "quran_results": quran_results,
                "hadith_results": hadith_results,
                "book_results": book_results,
                "book_content_results": book_content_results,
                "otherscience_results": otherscience_results,
                "fatwa_results": fatwa_results,
            }
            return all_query


def is_ajax(request):
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


def main_bar_search_view(request):
    ctx = {}
    url_parameter = request.GET.get("q")

    if url_parameter:
        quran_results = Ayat.objects.filter(text_without_tashkil__icontains=url_parameter)[:3]
        hadith_results = Hadith.objects.filter(text_without_tashkil__icontains=url_parameter)[:3]
        book_results = Book.objects.filter(title__icontains=url_parameter)[:3]
    else:
        quran_results = []
        hadith_results = []
        book_results = []

    ctx["quran_results"] = quran_results
    ctx["hadith_results"] = hadith_results
    ctx["book_results"] = book_results
    ctx["ayat_tafsir"] = AyatTafsirVideo.objects.filter(status=STATUS_PUBLISHED).all()
    ctx["query"] = url_parameter
    if is_ajax(request=request):
        html = render_to_string(template_name="search-results-partial.html", context=ctx)
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    return render(request, "home.html", context=ctx)

class SearchApi(APIView):

    def get_queryset(self):
        request = self.request
        query = request.GET
        sentence = query.get("q")
        sura = query.get("quran")
        hadith_book_id = query.get("hadith_book_id")
        book = query.get("book")

        qurancheck = query.get("qurancheck")
        hadithcheck = query.get("hadithcheck")
        bookcheck = query.get("bookcheck")
        othersciencecheck = query.get("othersciencecheck")
        fatwacheck = query.get("fatwacheck")

        # if searching from main search bar will search in all topics
        if query.get("mainq"):
            sentence = query.get("mainq")
            qurancheck = hadithcheck = bookcheck = othersciencecheck = fatwacheck = "on"

        if sentence:
            # query for quran
            if qurancheck:
                if sura:
                    quran_results = Ayat.objects.filter(text_without_tashkil__icontains=sentence, sura_id=sura)
                else:
                    quran_results = Ayat.objects.filter(text_without_tashkil__icontains=sentence)
            else:
                quran_results = []

            # query for hadith
            if hadithcheck:
                if hadith_book_id:

                    hadith_results = Hadith.objects.filter(text_without_tashkil__icontains=sentence, id=hadith_book_id)
                else:
                    hadith_results = Hadith.objects.filter(text_without_tashkil__icontains=sentence)
            else:
                hadith_results = []

            # query for books
            if bookcheck:
                if book:
                    book_results = Book.objects.filter(title__icontains=sentence, id=book)
                    book_content_results = BookSeach.objects.filter(book=book, key__icontains=sentence).all()
                else:
                    book_results = Book.objects.filter(title__icontains=sentence)
                    book_content_results = BookSeach.objects.filter(key__icontains=sentence).all()
            else:
                book_results = []
                book_content_results = []

            # query for other sciences
            if othersciencecheck:
                otherscience_results = OtherScience.objects.filter(status=STATUS_PUBLISHED).filter(
                    title__icontains=sentence)
            else:
                otherscience_results = []

            # query for fatwa
            if fatwacheck:
                fatwa_results = Fatwa.objects.filter(status=STATUS_PUBLISHED).filter(title__icontains=sentence)
            else:
                fatwa_results = []
            # print("book_content_results", book_content_results)

            all_query = {
                "quran_results": AyatNameSerializer(quran_results, many=True).data,
                "hadith_results": HadithNameSerializer(hadith_results, many=True).data,
                "book_results": BookSerializer(book_results, many=True).data,
                "book_content_results": BookSeachSerializer(book_content_results, many=True).data,
                "otherscience_results": OtherScienceSerializer(otherscience_results, many=True).data,
                "fatwa_results": FatwaSerializer(fatwa_results, many=True).data,
            }
            if all_query:
                return all_query

    def get(self, request):
        data = self.get_queryset()
        return JsonResponse(data)

