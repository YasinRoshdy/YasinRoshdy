from django.urls import path, include
from rest_framework.routers import DefaultRouter
from base.models import General_information
from base.serializer import General_informationSerializer
from .api import (
    ArticalsListAPI,
    BookByIdAPI,
    BooksListAPI,
    ChapterByBookInAlSahehListAPI,
    HadithListByChapterAPI,
    HadithRetriveAPI,
    HomeViewSets,
    OtherScienceListBySubjectIdAPI,
    SessionsCategorysByTypeListAPI,
    SessionsListByCategoryAPI,
    SessionsRetriveAPI,
    SuraAyatListAPI,
    AyatTafsirAudioListAPI,
    AyatTafsirVideoListAPI,
    AyatTelawaListAPI,
    BookInAlSahehListAPI,
    CallUsCreateAPI,
    DailyPublishListAPI,
    FatwaListAPI,
    General_informationRetriveAPI,
    OtherScienceSubjectListAPI,
    PhoneNumbersListAPI,
    RelatedSitesListAPI,
    SuraDetailsViewSets,
    SuraListAPI,
    SuraNameListAPI,
    TafsirHadithInAlSahehAPI,
    basic_info_api,
)


from .views import (
    SearchView,
    main_bar_search_view,
    about_us,
    book_by_pk,
    books,
    fatwa,
    fatwa_media,
    home,
    other_science,
    other_science_subject,
    other_science_subject_video,
    other_science_audio,
    other_science_audio_subject,
    other_science_video,
    other_science_video_subject,
    quran,
    quran_media,
    quran_media_video_part,
    quran_sura,
    read_quran,
    saheh,
    saheh_book,
    saheh_chapter,
    saheh_media,
    session_media,
    sessions,
    sessions_quran,
    sessions_hadith,
    sessions_othersciences,
    sessions_type,
    articals,
    callus,
    policy,
    quran_media_read,
    related_sites,
    saheh_media_read,
    sessions_category,
    sessions_cat_quran,
    sessions_cat_hadith,
    sessions_cat_othersciences,
    SearchApi,
    sessions_pillars,
    sessions_cat_pillars
)

app_name = "base"
# cbv : CBV.as_view()
# fbv : property_details
# dynamic url  '/id:int'

# Views
urlpatterns = [
    path("", home, name="home"),
    path("read_quran", read_quran, name="read_quran"),
    path("quran", quran, name="quran"),
    path("quran/<int:sura_id>", quran_sura, name="quran_sura"),
    path("quran_media/telawa/<int:sura_number>", quran_media, name="quran_media_telawa"),
    path("quran_media/audio/<int:sura_number>", quran_media, name="quran_media_audio"),
    path("quran_media/video/<int:sura_number>", quran_media, name="quran_media_video"),
    path("quran_media/read/<int:sura_number>", quran_media_read, name="quran_media_read"),
    path("quran_media/video/tafsir/<int:tafsir_id>", quran_media_video_part, name="quran_media_video_part"),
    # saheh
    path("saheh", saheh, name="saheh"),
    path("saheh/book/<int:book_id>", saheh_book, name="saheh_book"),
    path("saheh/chapter/<int:chapter_id>", saheh_chapter, name="saheh_chapter"),
    #
    path("saheh_media/video/<int:hadith_number>", saheh_media, name="saheh_media_video"),
    path("saheh_media/audio/<int:hadith_number>", saheh_media, name="saheh_media_audio"),
    path("saheh_media/read/<int:hadith_number>", saheh_media_read, name="saheh_media_read"),
    #
    path("books", books, name="books"),
    path("articals", articals, name="artical"),
    # path("books_type/<str:type>", books_by_type, name="books_type"),
    path("book/<int:pk>", book_by_pk, name="book"),
    # other science , fatwa , session
    path("fatwa", fatwa, name="fatwa"),
    path("fatwa/audio/<int:fatwa_id>", fatwa_media, name="fatwa_media"),
    path("other_science", other_science, name="other_science"),
    path("other_science/<int:subject_id>", other_science_subject, name="other_science_subject"),
    path("other_science/video/<int:other_science_id>", other_science_subject_video, name="other_science_subject_video"),
    path("other_science_audio", other_science_audio, name="other_science_audio"),
    path("other_science_audio/<int:subject_id>", other_science_audio_subject, name="other_science_audio_subject"),
    path("other_science_video", other_science_video, name="other_science_video"),
    path("other_science_video/<int:subject_id>", other_science_video_subject, name="other_science_video_subject"),
    path("sessions", sessions, name="sessions"),
    path("sessions/<str:type>", sessions_type, name="sessions_type"),
    path("sessions/category/<str:type>/<str:category>", sessions_category, name="sessions_category"),
    path("session/video/<int:session_id>", session_media, name="session_media_video"),
    # new paths
    path("sessions_quran", sessions_quran, name="sessions_quran"),
    path("sessions_quran/category/<str:type>/<str:category>", sessions_cat_quran, name="sessions_cat_quran"),
    path("sessions_hadith", sessions_hadith, name="sessions_hadith"),
    path("sessions_hadith/category/<str:type>/<str:category>", sessions_cat_hadith, name="sessions_cat_hadith"),
    path("sessions_othersciences", sessions_othersciences, name="sessions_othersciences"),
    path("sessions_othersciences/category/<str:type>/<str:category>", sessions_cat_hadith, name="sessions_cat_hadith"),
    path("sessions_pillars", sessions_pillars, name="sessions_pillars"),
    path("sessions_pillars/category/<str:type>/<str:category>", sessions_cat_pillars, name="sessions_cat_pillars"),
    # general
    path("callus", callus, name="callus"),
    path("about_us", about_us, name="about_us"),
    path("related_site", related_sites, name="related_site"),
    path("policy", policy, name="policy"),
    # search
    path("search-results", SearchView.as_view(), name="search_results"),
    path("searchapi/", SearchApi.as_view(), name="search_data"),
    path("main-search", main_bar_search_view, name="main_search"),
    # general requestes
    # request prayer time by city
    # path("api/prayer/<str:city>", prayer_city, name="prayer_city"),
    #     api
    #     path("api/BookInAlSaheh",
    #          BookInAlSahehViewSet.as_view({'get': 'list'}), name="main_search"),
]

# API
urlpatterns += [
    # general api
    path("api/relatedSitesList", RelatedSitesListAPI.as_view(), name="RelatedSitesListAPI"),
    path("api/phoneNumbersList", PhoneNumbersListAPI.as_view(), name="PhoneNumbersListAPI"),
    path("api/generalInformation", General_informationRetriveAPI.as_view(), name="General_informationListAPI"),
    path("api/callUsCreate", CallUsCreateAPI.as_view(), name="CallUsCreateAPI"),
    path("api/dailyPublishList", DailyPublishListAPI.as_view(), name="DailyPublishListAPI"),
    # general api
    # start home
    path("api/home", HomeViewSets.as_view({"get": "get"}), name="HomeViewSets"),
    path("api/basicInfo", basic_info_api, name="BasicInfo"),
    # end  home
    # start quran
    path("api/sura", SuraDetailsViewSets.as_view({"get": "get"}), name="SuraDetailsViewSets"),
    path("api/suraNames", SuraNameListAPI.as_view(), name="SuraNameListAPI"),
    path("api/ayatList", SuraAyatListAPI.as_view(), name="AyatListAPI"),
    path("api/ayatTelawaList", AyatTelawaListAPI.as_view(), name="AyatTelawaListAPI"),
    path("api/ayatTafsirAudioList", AyatTafsirAudioListAPI.as_view(), name="AyatTafsirAudioListAPI"),
    path("api/ayatTafsirVideoList", AyatTafsirVideoListAPI.as_view(), name="AyatTafsirVideoListAPI"),
    path("api/suraList", SuraListAPI.as_view(), name="SuraListAPI"),
    # end quran
    # start hadith
    path("api/TafsirHadithInAlSaheh", TafsirHadithInAlSahehAPI.as_view(), name="TafsirHadithInAlSahehListAPI"),
    path("api/hadithListByChapter", HadithListByChapterAPI.as_view(), name="TafsirHadithInAlSahehListAPI"),
    path("api/hadithRetrive", HadithRetriveAPI.as_view(), name="HadithRetriveAPI"),
    path("api/chapterByBookInAlSahehList", ChapterByBookInAlSahehListAPI.as_view(), name="ChapterByBookInAlSahehListAPI"),
    path("api/bookInAlSahehList", BookInAlSahehListAPI.as_view(), name="BookInAlSahehListAPI"),
    # end hadith
    # start fataw
    path("api/fatwaList", FatwaListAPI.as_view(), name="FatwaListAPI"),
    # end fataw
    # start  other - science list
    path("api/otherScienceSubjectList", OtherScienceSubjectListAPI.as_view(), name="OtherScienceSubjectListAPI"),
    path("api/OtherScienceListBySubjectId", OtherScienceListBySubjectIdAPI.as_view(), name="OtherScienceListBySubjectIdAPI"),
    # end other - science list
    # start books and articals
    # path("api/BooksAndArticalsList", BooksAndArticalsListAPI.as_view(), name="BooksAndArticalsListAPI"),
    path("api/ArticalsList", ArticalsListAPI.as_view(), name="ArticalsListAPI"),
    path("api/BooksList", BooksListAPI.as_view(), name="BooksListAPI"),
    path("api/BookById", BookByIdAPI.as_view(), name="BookByIdAPI"),
    # end  books and articals
    # start sessions list
    path("api/SessionsCategorysListByType", SessionsCategorysByTypeListAPI.as_view(), name="SessionsCategorysByTypeListAPI"),
    path("api/SessionsListByCategory", SessionsListByCategoryAPI.as_view(), name="SessionsListByCategoryAPI"),
    path("api/SessionsRetrive", SessionsRetriveAPI.as_view(), name="SessionsRetriveAPI"),
    # end sessions list
    # end api
]
