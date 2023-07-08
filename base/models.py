import math

from django.contrib import admin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.forms import IntegerField
from django.urls import reverse
from django.utils.translation import gettext as _
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField
from filer.models.filemodels import File as FilerFile

from ckeditor.fields import RichTextField, CKEditorWidget
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
# from django.utils.safestring import SafeString


# from phonenumbers import PhoneNumber
from base.general.logic.general import en_to_ar, get_val, if_get, if_val, sizify
from base.utils import BookManager, BookQuerySet, get_page_count_pdf

# Create your models here.
STATUS_CHOICES = [
    ("p", _("Published")),
    ("n", _("Not Published")),
]
STATUS_PUBLISHED = "p"
STATUS_NOT_PUBLISHED = "n"
SESSIONS_TYPE = [
    ("quran", _("quran")),
    ("hadith", _("AlHadith")),
    ("OtherScience", _("OtherScience")),
    ("pillars", _("pillars")),
]
DAILY_PUBLISH_CHOICES = [
    ("aya", _("aya")),
    ("hadith", _("hadith")),
    ("fatwa", _("fatwa")),
    ("part_of_book", _("part of book")),
]
DAYOFMONTH = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
    (11, 11),
    (12, 12),
    (13, 13),
    (14, 14),
    (15, 15),
    (16, 16),
    (17, 17),
    (18, 18),
    (19, 19),
    (20, 20),
    (21, 21),
    (22, 22),
    (23, 23),
    (24, 24),
    (25, 25),
    (26, 26),
    (27, 27),
    (28, 28),
    (29, 29),
    (30, 30),
    (31, 31),
]

BOOK_TYPE = [("book", _("book")), ("artical", _("artical"))]
MEDIA_TYPE = [("video", _("video")), ("audio", _("audio"))]
TANZIL_LOCATION = [("Makkah", _("Makkah")), ("Medina", _("Medina"))]
PHONE_NUMBER_TYPE = [("telephon", _("telephon")), ("mobile", _("mobile")), ("fax", _("fax"))]


def check(val):
    if val:
        return val
    else:
        return ""


class RelatedSites(models.Model):
    site = models.URLField(_("site"))
    name = models.CharField(_("name"), max_length=80, blank=True, null=True)
    text = models.CharField(_("words"), max_length=10000, blank=True, null=True)
    image = FilerImageField(
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name=f'{_("perfect cover page size")} {_("height")}:310px - {_("width")}:1440px',
        related_name="RelatedSites_image",
    )

    def __str__(self) -> str:
        return f"{_('RelatedSites')} {self.name} "

    class Meta:
        verbose_name = _("RelatedSites")
        verbose_name_plural = _("RelatedSites")


class PhoneNumbers(models.Model):
    phone_number = models.CharField(_("phone_number"), max_length=20)
    phone_number_type = models.CharField(_("type"), max_length=20, choices=PHONE_NUMBER_TYPE)

    def __str__(self) -> str:
        return f"{_('phone_number')} {self.phone  } "

    @property
    def phone(self):
        return self.phone_number.replace("+", "") + "+"

    class Meta:
        verbose_name = _("phone numbers")
        verbose_name_plural = _("phone numbers")


class Email(models.Model):
    email = models.EmailField(_("email"), max_length=200)

    def __str__(self) -> str:
        return f"{_('email')} {self.email} "

    class Meta:
        verbose_name = _("email")
        verbose_name_plural = _("email")


class General_information(models.Model):
    # visitor_count = models.IntegerField(_("visitor_count"), default=0)
    instagram_link = models.URLField(_("instagram_link"), null=True, blank=True)
    facebook_link = models.URLField(_("facebook_link"), null=True, blank=True)
    twitter_link = models.URLField(_("twitter_link"), null=True, blank=True)
    youtube_link = models.URLField(_("youtube_link"), null=True, blank=True)

    google_play_link = models.URLField(_("google_play_link"), null=True, blank=True)
    app_store_link = models.URLField(_("app_store_link"), null=True, blank=True)

    about_sheikh_short = RichTextField(verbose_name=_("about_sheikh_short"), null=True, blank=True)
    about_mousa_short = RichTextField(verbose_name=_("about_mousa_short"), null=True, blank=True)
    about_sheikh = RichTextField(blank=True, null=True, verbose_name=_("about_sheikh"))
    about_mousa = RichTextField(blank=True, null=True, verbose_name=_("about_mousa"))

    privacy_policy = models.CharField(_("privacy policy"), blank=True, null=True, max_length=50000)
    cover_page = FilerImageField(
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name=f'{_("perfect cover page size")} {_("height")}:310px - {_("width")}:1440px',
        related_name="cover_page",
    )
    sheikh_img = FilerImageField(
        null=True, blank=True, on_delete=models.PROTECT, verbose_name=_("sheikh image about us"), related_name="sheikh_img"
    )
    mousa_img = FilerImageField(
        null=True, blank=True, on_delete=models.PROTECT, verbose_name=_("mousa image about us"), related_name="mousa_img"
    )

    def __str__(self) -> str:
        return f"{_('home')}   "

    class Meta:
        ordering = ["id"]
        verbose_name = _("home")
        verbose_name_plural = _("home")

    def has_add_permission(self):
        return General_information.objects.exists()


class CallUs(models.Model):
    name = models.CharField(_("name"), max_length=200)
    email = models.EmailField(_("email"))
    message = models.CharField(_("message"), max_length=1000)

    def __str__(self) -> str:
        return f"{_('CallUs')}|{_('name')}:{self.name}|{_('message')}:{self.message}"

    class Meta:
        verbose_name = _("calledUs")
        verbose_name_plural = _("calledUs")


class DailyPublish(models.Model):

    publish_type = models.CharField(
        _("publish_type"),
        max_length=16,
        choices=DAILY_PUBLISH_CHOICES,
    )

    content = models.CharField(_("content"), max_length=1000, blank=True, null=True)

    sura = models.ForeignKey("Sura", verbose_name=_("sura"), on_delete=models.PROTECT, blank=True, null=True)
    aya = models.ForeignKey("Ayat", on_delete=models.PROTECT, verbose_name=_("ayat"), blank=True, null=True)

    hadith = models.ForeignKey("Hadith", on_delete=models.PROTECT, verbose_name=_("hadith"), blank=True, null=True)
    book_in_alsaheh = models.ForeignKey(
        "BookInAlSaheh", on_delete=models.PROTECT, verbose_name=_("AlHadith/AlSaheh/books"), blank=True, null=True
    )
    chapter_in_alsaheh = models.ForeignKey(
        "ChapterInAlSaheh", on_delete=models.PROTECT, verbose_name=_("ChapterInAlSaheh"), blank=True, null=True
    )
    display_date = models.DateField(_("display date"), default= timezone.now)
    # day = models.IntegerField(_("day"), choices=DAYOFMONTH, validators=[MaxValueValidator(31), MinValueValidator(1)])
    status = models.CharField(_("publish status"), max_length=1, choices=STATUS_CHOICES, default="p")

    class Meta:
        ordering = ["display_date", "publish_type"]
        get_latest_by = ["display_date", "publish_type"]

        verbose_name = _("Daily publishes")
        verbose_name_plural = _("Daily publishes")

        unique_together = (
            "publish_type",
            "display_date",
            # "day",
            "status",
        )

    def __str__(self) -> str:
        content = (
            self.content
            if (self.publish_type == "fatwa" or self.publish_type == "part_of_book") and self.content
            else self.aya.text
            if self.aya and self.content == "aya"
            else self.hadith and self.hadith.text
        )
        content = content if content else ""

        return f"{_('DailyPublish')}:{_('display date')}{self.display_date}|{_(self.publish_type)}|{content}"


# class DailyGroup(models.Model):
#     # model fields here
#     hadith = models.CharField(max_length=400, blank=True, null=True)
#     class Meta:
#         managed = False
#     def save(self, *args, **kwargs):
#         hadeath = kwargs["hadeath"]
#         if hadeath is not None:
#             obj = DailyPublish(publish_type="hadeth", content=hadeath, date=date)
#         return


class Fatwa(models.Model):

    title = models.CharField(_("title"), max_length=200, null=False)
    file = FilerFileField(on_delete=models.PROTECT, verbose_name=_("file"), null=True, blank=True)

    text = models.CharField(_("fatwa_text"), null=True, blank=True, max_length=20000)
    status = models.CharField(_("publish status"), max_length=1, choices=STATUS_CHOICES, default="p")

    def __str__(self) -> str:
        return f"{_('fatwa')} {self.title}"

    class Meta:
        verbose_name = _("Fatwas")
        verbose_name_plural = _("Fatwas")


class Book(models.Model):
    title = models.CharField(_("title"), max_length=255)
    cover = FilerImageField(
        related_name="book_covers",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("cover"),
    )
    file = FilerFileField(on_delete=models.PROTECT, verbose_name=_("file"), null=True, blank=True)

    page_count = models.IntegerField(_("page_count"), blank=True, null=True)

    type = models.CharField(_("type"), max_length=10, choices=BOOK_TYPE)

    status = models.CharField(_("publish status"), max_length=1, choices=STATUS_CHOICES, default="p")
    objects = BookQuerySet.as_manager()

    def save(self, *args, **kwargs):
        if self.file:
            self.page_count = get_page_count_pdf(self.file.file.path)

        # call the save() method of the parent
        super(Book, self).save(*args, **kwargs)

    @property
    def size(self):
        if not self.file:
            return ""
        return sizify(self.file.file.size)

    def __str__(self) -> str:
        get_count = if_get(if_val(self.page_count), f'{_("page_count")} {self.page_count}')
        return f"{_('Book')} | {_('type')} {_(self.type)}    | {self.title}  |{get_count} {self.size}"

    def get_absolute_url(self):
        return reverse("base:book", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = _("books and articles")
        verbose_name_plural = _("books and articles")
        ordering = ("type", "title")


class BookSeach(models.Model):
    key = models.CharField(_("key search"), max_length=400)
    book = models.ForeignKey("Book", verbose_name=_("BookInAlSaheh"), on_delete=models.PROTECT, null=True, blank=True, related_name="chapter")
    page = models.IntegerField(validators=[MaxValueValidator(500), MinValueValidator(1)])

    def __str__(self) -> str:
        return f"{_('BookFiles')} {_('book name')}:{self.book.title}|{_('page number')}:{self.page}|{_('search key')}:{self.key} "

    class Meta:
        verbose_name = _("Book Index")
        verbose_name_plural = _("Book Index")


class OtherScienceSubject(models.Model):
    subjects = models.CharField(_("subjects"), max_length=300)
    file_type = models.CharField(_("file_type"), max_length=12, choices=MEDIA_TYPE)
    status = models.CharField(_("publish status"), max_length=1, choices=STATUS_CHOICES, default="p")
    order = models.IntegerField(_('order'), null=True)

    class Meta:
        verbose_name = _("OtherScienceSubject")
        verbose_name_plural = _("OtherScienceSubject")
        ordering = ["-subjects"]

    def __str__(self) -> str:

        return f"{_('subjects')}:{self.subjects} |{_('file_type')}:{_(f'{self.file_type}')}  {_('OtherScienceSubject')}  "


class OtherScience(models.Model):
    title = models.CharField(_("title"), max_length=255)
    file = FilerFileField(on_delete=models.PROTECT, verbose_name=_("content"))
    subject = models.ForeignKey("OtherScienceSubject", verbose_name=_("OtherScienceSubject"), on_delete=models.PROTECT)
    status = models.CharField(_("publish status"), max_length=1, choices=STATUS_CHOICES, default="p")
    video_url = models.URLField(_("youtube_link"), null=True, blank=True)
    order_by = models.IntegerField(_("order") ,default=1)
    def __str__(self) -> str:

        return f"{_('title')}:{self.title} |{_('subject')}:{self.subject} {_('OtherScience')}  "

    class Meta:
        verbose_name = _("OtherScience")
        verbose_name_plural = _("OtherScience")
        ordering = ["subject", "title"]


class SessionsCategory(models.Model):
    name = models.CharField(_("title"), max_length=255)
    type = models.CharField(_("type"), max_length=20, choices=SESSIONS_TYPE)
    order = models.IntegerField(_("order"), null=True, blank=True)
    active_flag = models.BooleanField(_("active flag"), default=True)
    def __str__(self) -> str:
        return f"{_('SessionsCategory')} {self.name}:{_('type')}:{_(self.type)} "

    class Meta:
        verbose_name = _("SessionsCategory")
        verbose_name_plural = _("SessionsCategory")
        ordering = ["order", "type", "name"]


class Sessions(models.Model):
    title = models.CharField(_("title"), max_length=255)
    type = models.CharField(_("type"), max_length=20, choices=SESSIONS_TYPE)
    file = FilerFileField(on_delete=models.PROTECT, verbose_name=_("Content"))
    video_url = models.CharField(_("youtube_link"), max_length=255, null=True, blank=True)
    status = models.CharField(_("publish status"), max_length=1, choices=STATUS_CHOICES, default="p")
    category = models.ForeignKey(SessionsCategory, null=True, blank=True, on_delete=models.PROTECT, verbose_name=_("category"))
    order_by = models.IntegerField(_("order"),default=1)

    def __str__(self) -> str:
        return f"{_('Sessions')} {_('title')} {_('order')}:{self.title}  {self.category} {self.order_by}"

    class Meta:
        verbose_name = _("Sessions")
        verbose_name_plural = _("sessions")
        ordering = ["type", "category", "file__folder", "title", "id"]


# # class PrayTime(models.Model):

# #     Fajr = models.TimeField(_("Fajr"), null=True)
# #     Sunrise = models.TimeField(_("Sunrise"), null=True)
# #     Dhuhr = models.TimeField(_("Dhuhr"), null=True)
# #     Asr = models.TimeField(_("Asr"), null=True)
# #     Maghrib = models.TimeField(_("Maghrib"), null=True)
# #     Isha = models.TimeField(_("Isha"), null=True)
# #     city = models.CharField(_("city"), max_length=50, null=True)
# #     country = models.CharField(_("country"), max_length=50, null=True)
# #     date = models.DateField(_("date"))
# #     hijri = models.CharField(_("hijri"), max_length=20, null=True, blank=True)

# #     def __str__(self) -> str:
# #         return f"{_('PrayTime')} { get_val(self.hijri)}"

# #     class Meta:
# #         verbose_name = _("PrayTime")
# #         verbose_name_plural = _("PrayTime")

#
class AyatTelawa(models.Model):
    sura = models.ForeignKey("Sura", verbose_name=_("sura"), on_delete=models.PROTECT, null=True, blank=True)
    # aya_start = models.IntegerField(_("tafsir_aya_start"), choices=aya_choices)
    # aya_end = models.IntegerField(_("tafsir_aya_end"), choices=aya_choices)
    aya_start = models.ForeignKey(
        "Ayat", verbose_name=_("tafsir_aya_start"), on_delete=models.PROTECT, related_name="AyatTelawaaya_start", null=True, blank=True
    )
    aya_end = models.ForeignKey(
        "Ayat", verbose_name=_("tafsir_aya_end"), on_delete=models.PROTECT, related_name="AyatTelawaaya_end", null=True, blank=True
    )

    telawa = FilerFileField(on_delete=models.PROTECT, null=True, blank=True, related_name="telawa_file", verbose_name=_("telawa"))

    status = models.CharField(_("publish status"), max_length=1, choices=STATUS_CHOICES, default="p")

    @property
    def aya_count(self):
        if self.aya_start and self.aya_end:

            return abs(self.aya_end.count - self.aya_start.count)
        else:
            return ""

    def __str__(self) -> str:
        return f"{_('AyatTelawa')} {_('from')}:{self.aya_start}|{_('aya_count')}:{self.aya_count}"

    class Meta:
        verbose_name = _("telawa")
        verbose_name_plural = _("telawa")


class AyatTafsirAudio(models.Model):
    sura = models.ForeignKey("Sura", verbose_name=_("sura"), on_delete=models.PROTECT, null=True, blank=True)

    aya_start = models.ForeignKey(
        "Ayat", verbose_name=_("tafsir_aya_start"), on_delete=models.PROTECT, related_name="AyatTafsirAudioaya_start", null=True, blank=True
    )
    aya_end = models.ForeignKey(
        "Ayat", verbose_name=_("tafsir_aya_end"), on_delete=models.PROTECT, related_name="AyatTafsirAudioaya_end", null=True, blank=True
    )

    sound_tafsir = FilerFileField(
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="sound_tafsir_file",
        verbose_name=_("sound_tafsir"),
    )
    text = models.CharField(_("tafsir_ayat_text"), max_length=500000, blank=True, null=True)

    status = models.CharField(_("publish status"), max_length=1, choices=STATUS_CHOICES, default="p")

    @property
    def aya_count(self):
        if self.aya_start and self.aya_end:

            return abs(self.aya_end.count - self.aya_start.count)
        else:
            return ""

    def __str__(self) -> str:
        return f"{_('AyatTafsir')} {_('from')}:{self.aya_start}|{_('aya_count')}:{self.aya_count}"

    class Meta:
        verbose_name = _("audio_tafsir")
        verbose_name_plural = _("audio_tafsir")


class AyatTafsirVideo(models.Model):
    sura = models.ForeignKey("Sura", verbose_name=_("sura"), on_delete=models.PROTECT, null=True, blank=True)
    # aya_start = models.IntegerField(_("tafsir_aya_start"), choices=aya_choices)
    # aya_end = models.IntegerField(_("tafsir_aya_end"), choices=aya_choices)
    aya_start = models.ForeignKey(
        "Ayat", verbose_name=_("tafsir_aya_start"), on_delete=models.PROTECT, related_name="AyatTafsirVideoaya_start", null=True, blank=True
    )
    aya_end = models.ForeignKey(
        "Ayat", verbose_name=_("tafsir_aya_end"), on_delete=models.PROTECT, related_name="AyatTafsirVideoaya_end", null=True, blank=True
    )

    video_tafsir = FilerFileField(
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="video_tafsir_fileAyatTafsirVideo",
        verbose_name=_("video_tafsir_file"),
    )
    video_url = models.URLField(_("video_url"), max_length=400, null=True, blank=True)

    text = models.CharField(_("tafsir_ayat_text"), max_length=500000, blank=True, null=True)

    status = models.CharField(_("publish status"), max_length=1, choices=STATUS_CHOICES, default="p")

    @property
    def aya_count(self):
        if self.aya_start and self.aya_end:

            return abs(self.aya_end.count - self.aya_start.count)
        else:
            return ""

    def __str__(self) -> str:
        return f"{_('AyatTafsir')} {_('from')}:{self.aya_start}|{_('aya_count')}:{self.aya_count}"

    class Meta:
        verbose_name = f'{_("video_tafsir")}'
        verbose_name_plural = f'{_("video_tafsir")}'
        ordering = ["sura", "aya_start"]


class Sura(models.Model):
    location = models.CharField(_("tanzil_location"), max_length=50, choices=TANZIL_LOCATION, null=True)
    number = models.IntegerField(_("number"))
    name = models.CharField(_("name"), max_length=50)
    ayas_count = models.IntegerField(_("ayas_count"), blank=False, null=True)

    def all_ayas_list(self):
        ayat = Ayat.objects.only("text").filter(sura=self).order_by("count").all()
        return ayat

    def all_ayas(self):
        ayat = self.all_ayas_list()

        if self.number == 1:
            ayat = ayat[1:]
        concat = ""
        # if self.name != "الفاتحة" or self.name != "التوبَة":
        #     concat = Ayat.objects.all().first().text + "\n"

        for aya in ayat:
            c = en_to_ar(aya.count)

            concat += f"<p id='quran_text_p' class='quran-text'> {aya.text} <span> ﴿{c}﴾ </span></p>"
        return concat

    # models.ForeignKey("Quran", verbose_name=_("Quran"), on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{_('Quran Tafsir and Telawa')}|{_('sura')}:{self.name}|  {_('name')}:{self.name}|{_('ayas_count')} :{self.ayas_count}"

    class Meta:
        verbose_name = _("Quran Tafsir and Telawa")
        verbose_name_plural = _("Sura")
        ordering = ["number"]


class Ayat(models.Model):

    count = models.IntegerField(_("aya_count"))

    text = models.CharField(_("text"), max_length=100000)
    text_without_tashkil = models.CharField(_("text without tashkel"), max_length=100000)
    sura = models.ForeignKey("Sura", verbose_name=_("sura"), on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{_('sura')}:{self.sura.name}|{_('aya')} {_('number')} : {self.count}| {_('text')} :{self.text} "

    class Meta:
        verbose_name = _("Ayats")
        verbose_name_plural = _("Ayats")
        ordering = ["sura", "count"]


class TafsirHadithInAlSaheh(models.Model):
    # text = models.CharField(_("text"), max_length=100000)
    # order = models.IntegerField(_("order"))
    # title = models.CharField(_("title"), max_length=500)
    book = models.ForeignKey("BookInAlSaheh", verbose_name=_("BookInAlSaheh"), on_delete=models.PROTECT)
    chapter = models.ForeignKey("ChapterInAlSaheh", verbose_name=_("ChapterInAlSaheh"), on_delete=models.PROTECT)
    hadith = models.ForeignKey("Hadith", verbose_name=_("hadith"), on_delete=models.PROTECT)
    text = models.CharField(_("tafsir_hadith_text"), max_length=100000, blank=True, null=True)

    # video_tafsir = models.ManyToManyField("File", verbose_name=_(""))
    # models.ManyToOneRel("File.Model", verbose_name=_(""), on_delete=models.PROTECT)
    # FilerFileField(
    #     on_delete=models.PROTECT, null=True, blank=True, related_name="video_hadith_file", verbose_name=_("video_tafsir")
    # )
    video_tafsir = FilerFileField(
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="TafsirHadithInAlSahehvideo_tafsir_file",
        verbose_name=_("video_tafsir"),
    )

    audio_tafsir = FilerFileField(
        on_delete=models.PROTECT, null=True, blank=True, related_name="audio_hadith_file", verbose_name=_("audio_tafsir")
    )
    video_url = models.URLField(_("video_url"), max_length=400)
    status = models.CharField(_("publish status"), max_length=1, choices=STATUS_CHOICES, default="p")

    class Meta:
        verbose_name = _("AlHadith")
        verbose_name_plural = _("AlHadith")

    def __str__(self):
        return f"{_('hadith')}:{self.hadith} "

    @admin.display()
    def str(self):
        return "this i sst"


class Hadith(models.Model):
    # id = models.AutoField(primary_key=True)
    text = models.CharField(_("text"), max_length=100000)
    text_without_tashkil = RichTextField(_("text without tashkel"), max_length=100000)
    number = models.IntegerField(_("Hadith") + " " + _("order"))
    book = models.ForeignKey("BookInAlSaheh", verbose_name=_("BookInAlSaheh"), on_delete=models.PROTECT)
    chapter = models.ForeignKey("ChapterInAlSaheh", verbose_name=_("ChapterInAlSaheh"), on_delete=models.PROTECT)

    class Meta:
        verbose_name = _("hadith in Al Saheh")
        verbose_name_plural = _("hadith in Al Saheh")
        ordering = ["number"]

    def __str__(self):
        return f"{_('text')}:{self.text[0:50]}|{_('number')}:{self.number}|{_('chapter')}:{self.chapter} "


class ChapterInAlSaheh(models.Model):
    name = models.CharField(_("chapter name"), max_length=500)
    # order = models.IntegerField(_("chapter order"))
    book = models.ForeignKey("BookInAlSaheh", verbose_name=_("BookInAlSaheh"), on_delete=models.PROTECT)
    name_without_tashkil = models.CharField(_("without tashkel" + " " + _("title")), max_length=500)

    class Meta:
        verbose_name = _("ChapterInAlSaheh")
        verbose_name_plural = _("ChapterInAlSaheh")
        ordering = ["book", "id"]

    def __str__(self):
        return self.name


class BookInAlSaheh(models.Model):
    name = models.CharField(_("book name"), max_length=500)
    # order = models.IntegerField(_("book order"))
    name_without_tashkil = models.CharField(_("without tashkel" + " " + _("title")), max_length=500)
    active_flag = models.BooleanField(default=True)
    order_by = models.IntegerField(_("order"),default=1)

    class Meta:
        verbose_name = _("AlHadith/AlSaheh/books")
        verbose_name_plural = _("AlHadith/AlSaheh/books")
        ordering = ["id"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.order_by or  self.order_by == 1:
            self.order_by = self.id
            super(BookInAlSaheh, self).save(*args, **kwargs)

# # import the File class to inherit from
# # from filer.models.filemodels import File

# # # we'll need to refer to filer settings
# # from filer import settings as filer_settings

# # # helpers Model


# # class Video(File):
# #     _icon = "video"
# #     file_type = "Video"

# #     @classmethod
# #     def matches_file_type(cls, iname, ifile, mime_type):
# #         video_types = [
# #             "application/vnd.dvb.ait",
# #             "video/x-sgi-movie",
# #             "video/mp4",
# #             "video/mpeg",
# #             "video/x-msvideo",
# #             "video/x-ms-wmv",
# #             "video/ogg",
# #             "video/webm",
# #             "video/quicktime",
# #         ]
# #         return mime_type in video_types


# # class Audio(File):
# #     _icon = "audio"
# #     file_type = "Audio"

# #     @classmethod
# #     def matches_file_type(cls, iname, ifile, mime_type):
# #         video_types = [
# #             "audio/basic",
# #             "auido/L24",
# #             "audio/mid",
# #             "audio/mpeg",
# #             "audio/mp4",
# #             "audio/ogg",
# #             "audio/vorbis",
# #             "audio/vorbis",
# #             "audio/x-mpegurl",
# #             "audio/vnd.rn-realaudio",
# #             "audio/x-aiff",
# #         ]
# #         return mime_type in video_types


# # # class Image(File):
# # #     _icon = "image"
# # #     file_type = "Image"

# # #     @classmethod
# # #     def matches_file_type(cls, iname, ifile, mime_type):
# # #         video_types = [
# # #             "image/bmp	",
# # #             "image/cis-cod",
# # #             "audio/mid",
# # #             "image/gif",
# # #             "image/ief",
# # #             "image/jpeg",
# # #             "image/pipeg",
# # #             "image/svg+xml",
# # #             "image/tiff",
# # #             "image/x-icon",
# # #             "image/x-rgb",
# # #             "image/x-xbitmap",
# # #             "image/x-xpixmap",
# # #             "image/x-xwindowdump",
# # #         ]
# # #         return mime_type in video_types


# # # extend filer to video type , image ,sound
# # class FilerVideoField(FilerFileField):
# #     default_model_class = Video


MODEL_LIST = [
    ("fatwa", _("Fatwas")),
    ("fatwa", _("Fatwas")),
]


# class MultipleFileFiller(models.Model):

#     model = models.CharField(max_length=50, choices=MODEL_LIST)
#     # id of element in
#     item_id = models.IntegerField(_("id"))
#     file = FilerFileField(on_delete=models.PROTECT, null=True, blank=True, related_name="file_filler", verbose_name=_("audio_tafsir"))
#     youtube = models.URLField(_("youtube"))

#     class Meta:
#         ordering = ["model"]

#         verbose_name = _("multiple files")
#         verbose_name_plural = _("multiple files")

#         unique_together = (
#             "model",
#             "item_id",
#             #    "status"
#         )
