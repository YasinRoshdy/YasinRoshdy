#        ******************************************************
#        ******************************************************
# Start  ****************************************************** API
import json
from django.http import QueryDict
from rest_framework.decorators import api_view
from rest_framework import serializers
from datetime import date
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response as ResponseRest
from rest_framework.request import Request as RequestRest
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.viewsets import ViewSet
from drf_yasg.utils import swagger_auto_schema, swagger_serializer_method
from drf_yasg import openapi
from filer.models.filemodels import File as FilerFile
from base.context_processors import basic_info
from base.general.logic.general import remove_None_vals, sizify
from base.general.logic.orm import get_file_data, get_file_url, get_filer
from base.models import (
    SESSIONS_TYPE,
    Ayat,
    AyatTafsirAudio,
    AyatTafsirVideo,
    AyatTelawa,
    Book,
    BookInAlSaheh,
    CallUs,
    ChapterInAlSaheh,
    DailyPublish,
    Fatwa,
    General_information,
    Hadith,
    OtherScience,
    OtherScienceSubject,
    RelatedSites,
    PhoneNumbers,
    Sessions,
    SessionsCategory,
    Sura,
    TafsirHadithInAlSaheh,
)

from base.serializer import (
    AyatTextSerializer,
    PhoneNumbersSerializer,
    RelatedSitesSerializer,
    AyatSerializer,
    AyatTafsirAudioSerializer,
    AyatTafsirVideoSerializer,
    AyatTelawaSerializer,
    BookInAlSahehSerializer,
    ChapterInAlSahehSerializer,
    CallUsSerializer,
    DailyPublishSerializer,
    General_informationSerializer,
    HadithSerializer,
    BookSerializer,
    OtherScienceSerializer,
    SessionCategorySerializer,
    SessionSerializer,
    SuraNameSerializer,
    SuraSerializer,
    EmailSerializer,
    FatwaSerializer,
    OtherScienceSubjectSerializer,
    TafsirHadithInAlSahehSerializer,
)


def api_message_not_found_for_this_input(praram):
    return f"You Must Send Right {praram} - Not Found - ."


def api_message_should_send_parameter(praram):
    return f"You Must Send  {praram} as parameter ."


def if_item_func(item, func):
    if item:
        return func(item)
    else:
        return None


# general hepers


def get_daily_publish(day=None):
    day = day or date.today()
    data = DailyPublish.objects.filter(display_day=day).all()
    ser = DailyPublishSerializer(data, many=True)
    res = []

    for daily in ser.data:
        res.append(remove_None_vals(daily))

    return res


# end general hepers


# general  api
class RelatedSitesListAPI(ListAPIView):
    serializer_class = RelatedSitesSerializer
    queryset = RelatedSites.objects.all()


class PhoneNumbersListAPI(ListAPIView):
    serializer_class = PhoneNumbersSerializer
    queryset = PhoneNumbers.objects.all()


class General_informationRetriveAPI(RetrieveAPIView):
    serializer_class = General_informationSerializer
    queryset = General_information.objects.all()

    def get(self, request):

        general_info = General_information.objects.first()
        if not general_info:
            return ResponseRest({"success": True, "data": "No Data Exist"})

        data = self.get_serializer(general_info).data
        data["cover_page"] = get_file_url(data["cover_page"])
        data["sheikh_img"] = get_file_url(data["sheikh_img"])
        data["mousa_img"] = get_file_url(data["mousa_img"])
        return ResponseRest({"success": True, "data": data})


class CallUsCreateAPI(CreateAPIView):
    serializer_class = CallUsSerializer
    queryset = CallUs.objects.all()


class DailyPublishListAPI(RetrieveAPIView):
    serializer_class = DailyPublishSerializer

    def get(self, request):
        return ResponseRest({"success": True, "data": get_daily_publish(request.query_params.get("day"))})


# general api
# start home

# will get basic info -which is the context in front -contains General info + visitor count , hijri date .
# @api_view(["GET"])
# def basic_info_api(request):
#     return basic_info()


@api_view(["GET"])
def basic_info_api(request):
    res = basic_info(request)
    return ResponseRest(data={"message": "success", "data": res})


# @api_view()
# def basic_info_api(request):
#     return ResponseRest({"message": "Hello, world!"})


class HomeViewSets(ViewSet):
    def get(self, request):
        daily_publish = get_daily_publish()
        general_data = General_information.objects.all().first()
        general = General_informationSerializer(general_data, many=False).data

        # print(general.pop("cover_page"))
        general["cover_page"] = if_item_func(general.get("cover_page"), get_file_url)
        general["sheikh_img"] = if_item_func(general.get("sheikh_img"), get_file_url)
        general["mousa_img"] = if_item_func(general.get("mousa_img"), get_file_url)

        return ResponseRest(
            {
                "success": True,
                "data": {
                    "daily": daily_publish,
                    "general": general,
                },
            }
        )


# end home

# start quran
class SuraDetailsViewSets(ViewSet):
    # # @swagger_auto_schema(
    # #     operation_description="Sura Details Get all ayas ordered and  with it's numbers",
    # #     request_body=openapi.Schema(
    # #         type=openapi.TYPE_OBJECT,
    # #         required=["sura_id"],
    # #         properties={"sura_id": openapi.Schema(type=openapi.TYPE_INTEGER)},
    # #     ),
    # #     security=[],
    # #     tags=["Users"],
    # # )
    # @swagger_auto_schema(
    #     # methods=["get"],
    #     manual_parameters=[
    #         openapi.Parameter("sura_id", openapi.TYPE_INTEGER, "test manual param", type=openapi.TYPE_INTEGER),
    #     ],
    #     responses={
    #         200: openapi.Response("response description", SuraSerializer(many=True), "all text"),
    #     },
    #     tags=["Suras"],
    # )
    def get(self, request: RequestRest):
        # sura_id = request.query_params.get("sura_id")

        try:
            sura_id = int(request.query_params.get("sura_id"))
            if not (sura_id and isinstance(sura_id, int)):
                raise Exception("SuraDetailsViewSets : sura_id and isinstance(sura_id, int)", sura_id, type(sura_id))
        except Exception:

            return ResponseRest(
                {"success": False, "message": api_message_should_send_parameter("sura_id:<int>")},
                status=HTTP_400_BAD_REQUEST,
            )

        sura: Sura = Sura.objects.filter(id=sura_id).first()
        if not sura:
            return ResponseRest({"success": False, "message": api_message_not_found_for_this_input("sura_id")}, status=HTTP_400_BAD_REQUEST)

        sura_ser = SuraSerializer(sura)
        data = sura_ser.data
        data["text"] = AyatTextSerializer(sura.all_ayas_list(), many=True).data
        return ResponseRest({"success": True, "data": data})


# to get all ayas data for single sura by sura_id
class SuraAyatListAPI(ListAPIView):
    serializer_class = AyatSerializer
    queryset = Ayat.objects.all()

    def get(self, request):
        try:
            sura_id = int(request.query_params.get("sura_id"))
            if not (sura_id and isinstance(sura_id, int)):
                raise Exception("SuraDetailsViewSets : sura_id and isinstance(sura_id, int)", sura_id, type(sura_id))
        except Exception:

            return ResponseRest(
                {"success": False, "message": api_message_should_send_parameter("sura_id:<int>")},
                status=HTTP_400_BAD_REQUEST,
            )
        ayas = self.get_queryset().order_by("count").filter(sura=sura_id)
        if not ayas or len(ayas) == 0:
            return ResponseRest({"success": False, "message": api_message_not_found_for_this_input("sura_id")}, status=HTTP_400_BAD_REQUEST)
        data = AyatSerializer(ayas, many=True).data
        return ResponseRest({"success": True, "data": data})


class SuraListAPI(ListAPIView):
    serializer_class = SuraSerializer
    queryset = Sura.objects.all()


class AyatTelawaListAPI(ListAPIView):
    serializer_class = AyatTelawaSerializer
    queryset = AyatTelawa.objects.all()

    def get(self, request):
        try:
            sura_id = int(request.query_params.get("sura_id"))
            if not (sura_id and isinstance(sura_id, int)):
                raise Exception("SuraDetailsViewSets : sura_id and isinstance(sura_id, int)", sura_id, type(sura_id))
        except Exception:

            return ResponseRest(
                {"success": False, "message": api_message_should_send_parameter("sura_id:<int>")},
                status=HTTP_400_BAD_REQUEST,
            )
        ayat = self.get_queryset().filter(sura=sura_id).all()
        if not ayat or len(ayat) == 0:
            return ResponseRest({"success": False, "message": api_message_not_found_for_this_input("sura_id")}, status=HTTP_400_BAD_REQUEST)

        ayat_telawa_list = AyatTelawaSerializer(ayat, many=True).data
        # res = []
        for item in ayat_telawa_list:

            file = get_file_url(item.get("telawa"))

            item["file"] = file
            del item["telawa"]

            item["aya_start_count"] = Ayat.objects.only("count").filter(id=item["aya_start"]).first().count
            item["aya_end_count"] = Ayat.objects.only("count").filter(id=item["aya_end"]).first().count

        return ResponseRest({"data": ayat_telawa_list, "success": True})


class AyatTafsirAudioListAPI(ListAPIView):
    serializer_class = AyatTafsirAudioSerializer
    queryset = AyatTafsirAudio.objects.all()

    def get(self, request):
        try:
            sura_id = int(request.query_params.get("sura_id"))
            if not (sura_id and isinstance(sura_id, int)):
                raise Exception("SuraDetailsViewSets : sura_id and isinstance(sura_id, int)", sura_id, type(sura_id))
        except Exception:

            return ResponseRest(
                {"success": False, "message": api_message_should_send_parameter("sura_id:<int>")},
                status=HTTP_400_BAD_REQUEST,
            )

        ayat = self.get_queryset().filter(sura=sura_id).all()
        if not ayat or len(ayat) == 0:
            return ResponseRest({"success": False, "message": api_message_not_found_for_this_input("sura_id")}, status=HTTP_400_BAD_REQUEST)

        ayat_telawa_list = AyatTafsirAudioSerializer(ayat, many=True).data
        # res = []
        for item in ayat_telawa_list:

            file = get_file_url(item.get("sound_tafsir"))

            item["file"] = file
            del item["sound_tafsir"]

            item["aya_start_count"] = Ayat.objects.only("count").filter(id=item["aya_start"]).first().count
            item["aya_end_count"] = Ayat.objects.only("count").filter(id=item["aya_end"]).first().count

        return ResponseRest({"data": ayat_telawa_list, "success": True})


class AyatTafsirVideoListAPI(ListAPIView):
    serializer_class = AyatTafsirVideoSerializer
    queryset = AyatTafsirVideo.objects.all()

    def get(self, request):
        try:
            sura_id = int(request.query_params.get("sura_id"))
            if not (sura_id and isinstance(sura_id, int)):
                raise Exception("SuraDetailsViewSets : sura_id and isinstance(sura_id, int)", sura_id, type(sura_id))
        except Exception:

            return ResponseRest(
                {"success": False, "message": api_message_should_send_parameter("sura_id:<int>")},
                status=HTTP_400_BAD_REQUEST,
            )

        ayat = self.get_queryset().filter(sura=sura_id).all()
        if not ayat or len(ayat) == 0:
            return ResponseRest({"success": False, "message": api_message_not_found_for_this_input("sura_id")}, status=HTTP_400_BAD_REQUEST)

        data = AyatTafsirVideoSerializer(ayat, many=True).data
        # res = []
        for item in data:

            file = get_file_url(item.get("video_tafsir"))

            item["file"] = file
            item.pop("video_tafsir")
            # del item["video_tafsir"]
            item["aya_start_count"] = Ayat.objects.only("count").filter(id=item["aya_start"]).first().count
            item["aya_end_count"] = Ayat.objects.only("count").filter(id=item["aya_end"]).first().count
        return ResponseRest({"success": True, "data": data})


class SuraNameListAPI(ListAPIView):
    serializer_class = SuraNameSerializer
    queryset = Sura.objects.values("name", "number")


# end quran

# start hadith
class TafsirHadithInAlSahehAPI(RetrieveAPIView):
    serializer_class = TafsirHadithInAlSahehSerializer
    queryset = TafsirHadithInAlSaheh.objects.all()

    def get(self, request):
        try:
            hadith_id = int(request.query_params.get("hadith_id"))
            if not (hadith_id and isinstance(hadith_id, int)):
                raise Exception("SuraDetailsViewSets : hadith_id and isinstance(hadith_id, int)", hadith_id, type(hadith_id))
        except Exception:

            return ResponseRest(
                {"success": False, "message": api_message_should_send_parameter("hadith_id:<int>")},
                status=HTTP_400_BAD_REQUEST,
            )

        tafsir_hadth = TafsirHadithInAlSaheh.objects.filter(hadith_id=hadith_id).first()
        if not tafsir_hadth:
            return ResponseRest(
                {"success": False, "message": api_message_not_found_for_this_input("hadith_id")},
                status=HTTP_400_BAD_REQUEST,
            )
        data = TafsirHadithInAlSahehSerializer(tafsir_hadth).data

        data["video_tafsir"] = get_file_url(data["video_tafsir"])
        data["audio_tafsir"] = get_file_url(data["audio_tafsir"])

        return ResponseRest({"success": True, "data": data})


class HadithRetriveAPI(RetrieveAPIView):
    serializer_class = HadithSerializer
    queryset = Hadith.objects.all()

    def get(self, request):
        try:
            hadith_id = int(request.query_params.get("hadith_id"))
            if not (hadith_id and isinstance(hadith_id, int)):
                raise Exception("SuraDetailsViewSets : hadith_id and isinstance(hadith_id, int)", hadith_id, type(hadith_id))
        except Exception:
            return ResponseRest(
                {"success": False, "message": api_message_should_send_parameter("hadith_id:<int>")},
                status=HTTP_400_BAD_REQUEST,
            )

        hadith = Hadith.objects.filter(id=hadith_id)
        if not hadith:
            return ResponseRest({"success": False, "message": api_message_not_found_for_this_input("hadith_id")}, status=HTTP_400_BAD_REQUEST)

        data = HadithSerializer(hadith).data

        return ResponseRest({"success": True, "data": data})


class HadithListByChapterAPI(ListAPIView):
    serializer_class = HadithSerializer
    queryset = Hadith.objects.all()

    def get(self, request):

        try:
            chapter_id = int(request.query_params.get("chapter_id"))
            if not (chapter_id and isinstance(chapter_id, int)):
                raise Exception("SuraDetailsViewSets : chapter_id and isinstance(chapter_id, int)", chapter_id, type(chapter_id))
        except Exception:

            return ResponseRest(
                {"success": False, "message": api_message_should_send_parameter("chapter_id:<int>")},
                status=HTTP_400_BAD_REQUEST,
            )

        hadiths = Hadith.objects.filter(chapter_id=chapter_id).all()
        if not hadiths or len(hadiths) == 0:
            return ResponseRest({"success": False, "message": api_message_not_found_for_this_input("chapter_id")}, status=HTTP_400_BAD_REQUEST)

        data = HadithSerializer(hadiths, many=True).data
        return ResponseRest({"success": True, "data": data})


class ChapterByBookInAlSahehListAPI(ListAPIView):
    serializer_class = ChapterInAlSahehSerializer
    queryset = ChapterInAlSaheh.objects.all()

    def get(self, request):
        try:
            book_id = int(request.query_params.get("book_id"))
            if not (book_id and isinstance(book_id, int)):
                raise Exception("SuraDetailsViewSets : book_id and isinstance(book_id, int)", book_id, type(book_id))
        except Exception:

            return ResponseRest(
                {"success": False, "message": api_message_should_send_parameter("book_id:<int>")},
                status=HTTP_400_BAD_REQUEST,
            )

        chapters = ChapterInAlSaheh.objects.filter(book_id=book_id).all()
        if not chapters or len(chapters) == 0:
            return ResponseRest({"success": False, "message": api_message_not_found_for_this_input("book_id")}, status=HTTP_400_BAD_REQUEST)

        data = ChapterInAlSahehSerializer(chapters, many=True).data
        return ResponseRest({"success": True, "data": data})


class BookInAlSahehListAPI(ListAPIView):
    serializer_class = BookInAlSahehSerializer
    queryset = BookInAlSaheh.objects.all()


class SuraListAPI(ListAPIView):
    serializer_class = SuraSerializer
    queryset = Sura.objects.all()


# end hadith

# start fatwa


class FatwaListAPI(ListAPIView):
    serializer_class = FatwaSerializer
    queryset = Fatwa.objects.all()

    def get(self, request):

        queryset = self.get_queryset()
        data = FatwaSerializer(queryset, many=True).data

        for el in data:

            el["file"] = get_file_url(el.get("file"))

        return ResponseRest({"success": True, "data": data})


#   end fatwa

# start other-science


class OtherScienceSubjectListAPI(ListAPIView):
    serializer_class = OtherScienceSubjectSerializer
    queryset = OtherScienceSubject.objects.all()


class OtherScienceListBySubjectIdAPI(ListAPIView):
    serializer_class = OtherScienceSerializer
    queryset = OtherScience.objects.all()

    def get(self, request):
        try:
            subject_id = int(request.query_params.get("subject_id"))
            if not (subject_id and isinstance(subject_id, int)):
                raise Exception("SuraDetailsViewSets : subject_id and isinstance(subject_id, int)", subject_id, type(subject_id))
        except Exception:
            return ResponseRest(
                {"success": False, "message": api_message_should_send_parameter("subject_id:<int>")},
                status=HTTP_400_BAD_REQUEST,
            )

        res = OtherScience.objects.filter(subject_id=subject_id).all()
        _data = OtherScienceSerializer(res, many=True).data

        # if isinstance(data, QueryDict):  # optional
        #     data._mutable = True
        # data = json.loads(json.dumps(_data))

        for el in _data:
            el["file"] = get_file_url(el.get("file"))

        return ResponseRest({"success": True, "data": _data})


# end other-science

# start session


class SessionsCategorysByTypeListAPI(ListAPIView):
    serializer_class = SessionCategorySerializer
    queryset = SessionsCategory.objects.all()

    def get(self, request):
        try:
            _type = request.query_params.get("type")

            if not (_type and isinstance(_type, str) and _type in [el[0] for el in SESSIONS_TYPE]):
                raise Exception("SuraDetailsViewSets : type and isinstance(type, str)", _type, type(_type))
        except Exception:

            return ResponseRest(
                {"success": False, "message": api_message_should_send_parameter(f"type:<str> on of list {[el[0] for el in SESSIONS_TYPE]}")},
                status=HTTP_400_BAD_REQUEST,
            )

        res = SessionsCategory.objects.filter(type=_type).all()

        data = SessionCategorySerializer(res, many=True).data

        return ResponseRest({"success": True, "data": data})


class SessionsListByCategoryAPI(ListAPIView):
    serializer_class = SessionSerializer
    queryset = Sessions.objects.all()

    def get(self, request):
        try:
            category_id = int(request.query_params.get("category_id"))
            if not (category_id and isinstance(category_id, int)):
                raise Exception("SuraDetailsViewSets : category_id and isinstance(category_id, int)", category_id, type(category_id))
        except Exception:

            return ResponseRest(
                {"success": False, "message": api_message_should_send_parameter("category_id:<int>")},
                status=HTTP_400_BAD_REQUEST,
            )

        res = Sessions.objects.filter(status="p", category_id=category_id).first()
        data = SessionSerializer(res, many=False).data

        data["file"] = get_file_url(data.get("file"))
        return ResponseRest({"success": True, "data": data})


class SessionsRetriveAPI(RetrieveAPIView):
    serializer_class = SessionSerializer
    queryset = Sessions.objects.all()

    def get(self, request):
        try:
            session_id = int(request.query_params.get("session_id"))
            if not (session_id and isinstance(session_id, int)):
                raise Exception("SuraDetailsViewSets : haditsession_idh_id and isinstance(session_id, int)", session_id, type(session_id))
        except Exception:

            return ResponseRest(
                {"success": False, "message": api_message_should_send_parameter("session_id:<int>")},
                status=HTTP_400_BAD_REQUEST,
            )

        session = Sessions.objects.filter(id=session_id)
        if not session:
            return ResponseRest({"success": False, "message": api_message_not_found_for_this_input("session_id")}, status=HTTP_400_BAD_REQUEST)

        data = SessionSerializer(session).data
        data["file"] = get_file_url(data.get("file"))
        return ResponseRest({"success": True, "data": data})


# end session

#     def list(self, request):
#         return ResponseRest(self.serializer.data)


# # END API


# books and articals


# class BooksAndArticalsListAPI(ListAPIView):
#     serializer_class = BookSerializer
#     queryset = Book.objects.all()


class ArticalsListAPI(ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get(self, request):
        res = self.get_queryset().filter(type="artical").all()
        data = BookSerializer(res, many=True).data

        for item in data:
            item["cover"] = get_file_url(item.get("cover"))
            fdata = get_file_data(item["file"])
            item["file"] = get_file_url(item.get("file"))
            item["file_data"] = fdata

        return ResponseRest({"success": True, "data": data})


class BooksListAPI(ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get(self, request):
        res = Book.objects.filter(type="book").all()
        data = BookSerializer(res, many=True).data

        for item in data:
            fd = get_file_data(item["file"])

            item["cover"] = get_file_url(item.get("cover"))
            item["file"] = get_file_url(item.get("file"))
            item["file_data"] = fd

        return ResponseRest({"success": True, "data": data})


class BookByIdAPI(RetrieveAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get(self, request):
        try:
            book_id = int(request.query_params.get("book_id"))
            if not (book_id and isinstance(book_id, int)):
                raise Exception("SuraDetailsViewSets : book_id and isinstance(book_id, int)", book_id, type(book_id))
        except Exception:

            return ResponseRest(
                {"success": False, "message": api_message_should_send_parameter("book_id:<int>")},
                status=HTTP_400_BAD_REQUEST,
            )
        book = Book.objects.get(id=book_id)
        data = BookSerializer(book, many=False).data
        fd = get_file_data(data["file"])
        data["cover"] = get_file_url(data.get("cover"))

        data["file_data"] = fd

        return ResponseRest({"success": True, "data": data})
