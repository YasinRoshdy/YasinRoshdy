from random import random

from django import forms
from django.contrib import admin
from django.utils.translation import gettext as _
from base.forms import AyatTafsirAudioForm, AyatTafsirVideoForm, GeneralInfoForm, HadithTafsirForm
from dynamic_select.admin import DynamicModelAdminMixin

from base.models import (
    Ayat,
    AyatTafsirVideo,
    AyatTafsirAudio,
    AyatTelawa,
    Book,
    BookInAlSaheh,
    BookSeach,
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
    RelatedSites,
    Sessions,
    SessionsCategory,
    Sura,
    TafsirHadithInAlSaheh,
)

# from .models import City, Country, Person


# Start Test
# @admin.register(City)
# class CityAdmin(admin.ModelAdmin):
#     pass


# @admin.register(Country)
# class CountryAdmin(admin.ModelAdmin):
#     pass


# @admin.register(Person)
# class PersonAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
#     fields = ("name", "country", "city",)
#     dynamic_fields = ("city",)

#     def get_dynamic_city_field(self, data):
#         queryset = City.objects.filter(country=data.get("country"))
#         value = data.get("city")

#         if value not in queryset:
#             value = queryset.first()

#         return queryset, value


# End Test
# from base.forms import DailyGroupForm
# from dynamic_admin_forms.admin import DynamicModelAdminMixin
admin.site.disable_action("delete_selected")

# class DailyGroupAdmin(admin.ModelAdmin):

#     form = DailyGroupForm

#     fieldsets = (
#         (
#             None,
#             {
#                 "fields": (
#                     "date",
#                     "hadeath",
#                     "aya",
#                     "fatwa",
#                     "part_of_book",
#                 ),
#             },
#         ),
#     )

# admin.site.register(DailyPublish, DailyGroupAdmin)
# admin.site.register(DailyGroup)


@admin.action(description=_("Mark selected as published"))
def publish(modeladmin, request, queryset):
    queryset.update(status="p")


@admin.action(description=_("Mark selected as not published"))
def cancel_publish(modeladmin, request, queryset):
    queryset.update(status="n")


# class DailyPublishAdmin(admin.ModelAdmin):

#     actions = [publish]

#     list_filter = ["publish_type", "status"]

#     def get_action_choices(self, request):
#         choices = super(DailyPublishAdmin, self).get_action_choices(request)
#         # super(DailyPublish, self).get_action_choices(request)
#         # choices is a list, just change it.
#         # the first is the BLANK_CHOICE_DASH
#         choices.pop(0)
#         # do something to change the list order
#         # the first one in list will be default option
#         choices.reverse()
#         return choices


# admin.site.register(DailyPublish, DailyPublishAdmin)


@admin.register(DailyPublish)
class DailyPublishAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    actions = [publish]
    list_filter = ["status"]
    fields = ("publish_type", "content", "sura", "aya", "book_in_alsaheh", "chapter_in_alsaheh", "hadith", "display_date", "status")
    dynamic_fields = (
        "aya",
        "chapter_in_alsaheh",
        "hadith",
    )

    def get_dynamic_aya_field(self, data):
        if not data.get("sura"):
            return Ayat.objects.none(), ""
        queryset = Ayat.objects.filter(sura=data.get("sura"))
        value = data.get("aya")

        if value not in queryset:
            value = queryset.first()

        return queryset, value

    def get_dynamic_chapter_in_alsaheh_field(self, data):
        if not data.get("book_in_alsaheh"):
            return ChapterInAlSaheh.objects.none(), ""
        queryset = ChapterInAlSaheh.objects.filter(book=data.get("book_in_alsaheh"))
        value = data.get("chapter_in_alsaheh")

        if value not in queryset:
            value = ""

        return queryset, value

    def get_dynamic_hadith_field(self, data):
        if not data.get("book_in_alsaheh") and not data.get("chapter_in_alsaheh"):
            return Hadith.objects.none(), ""
        queryset = Hadith.objects.filter(book=data.get("book_in_alsaheh"), chapter=data.get("chapter_in_alsaheh"))
        value = data.get("hadith")

        if value not in queryset:
            value = queryset.first()

        return queryset, value

    def get_action_choices(self, request):
        choices = super(DailyPublishAdmin, self).get_action_choices(request)
        choices.pop(0)
        choices.reverse()
        return choices


class FatwaAdmin(admin.ModelAdmin):
    actions = [publish]
    list_filter = ["status"]

    def get_action_choices(self, request):
        choices = super(FatwaAdmin, self).get_action_choices(request)
        choices.pop(0)
        choices.reverse()
        return choices


admin.site.register(Fatwa, FatwaAdmin)

# aya_choices = [(i, f'{i}')for i in range(1, 285)]


# class AyatTafsirForm(forms.ModelForm):

#     class Meta:
#         model = AyatTafsir
#         fields = "__all__"
#         aya_start = forms.ChoiceField(
#             choices=aya_choices)


@admin.register(AyatTafsirVideo)
class AyatTafsirVideoAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    fields = (
        "sura",
        "aya_start",
        "aya_end",
        "text",
        "video_tafsir",
        "video_url",
        "status",
    )
    dynamic_fields = ("aya_start", "aya_end")
    form = AyatTafsirVideoForm
    actions = [publish]
    list_filter = ["status", "sura"]
    # search_fields = ["sura_name", "video_tafsir_name"]
    ordering = (
        "sura",
        "aya_start",
    )

    def get_dynamic_aya_start_field(self, data):
        if not data.get("sura"):
            return Ayat.objects.none(), ""
        queryset = Ayat.objects.filter(sura=data.get("sura"))
        value = data.get("aya_start")

        if value not in queryset:
            value = queryset.first()

        return queryset, value

    def get_dynamic_aya_end_field(self, data):

        if not data.get("sura"):
            return Ayat.objects.none(), ""

        queryset = Ayat.objects.filter(sura=data.get("sura"))
        aya_end = data.get("aya_end")

        if aya_end not in queryset:
            aya_end = queryset.last()

        # aya_start = data.get('sura')
        # if aya_start.count < aya_end.count:
        #     return queryset, aya_start

        return queryset, aya_end

    def get_action_choices(self, request):
        choices = super(AyatTafsirVideoAdmin, self).get_action_choices(request)
        choices.pop(0)
        choices.reverse()
        return choices


@admin.register(AyatTafsirAudio)
class AyatTafsirAudioAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    fields = (
        "sura",
        "aya_start",
        "aya_end",
        "text",
        "sound_tafsir",
        "status",
    )
    dynamic_fields = (
        "aya_start",
        "aya_end",
    )
    form = AyatTafsirAudioForm
    actions = [publish]
    list_filter = ["status", "sura"]
    ordering = (
        "sura",
        "aya_start",
    )

    def get_dynamic_aya_start_field(self, data):
        if not data.get("sura"):
            return Ayat.objects.none(), ""
        queryset = Ayat.objects.filter(sura=data.get("sura"))
        value = data.get("aya_start")

        if value not in queryset:
            value = queryset.first()

        return queryset, value

    def get_dynamic_aya_end_field(self, data):

        if not data.get("sura"):
            return Ayat.objects.none(), ""

        queryset = Ayat.objects.filter(sura=data.get("sura"))
        aya_end = data.get("aya_end")

        if aya_end not in queryset:
            aya_end = queryset.last()

        return queryset, aya_end

    def get_action_choices(self, request):
        choices = super(AyatTafsirAudioAdmin, self).get_action_choices(request)
        choices.pop(0)
        choices.reverse()
        return choices


@admin.register(AyatTelawa)
class AyatTelawaAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    fields = (
        "sura",
        "aya_start",
        "aya_end",
        "telawa",
        "status",
    )
    dynamic_fields = (
        "aya_start",
        "aya_end",
    )
    ordering = (
        "sura",
        "aya_start",
    )
    actions = [publish]
    list_filter = ["status", "sura"]

    def get_dynamic_aya_start_field(self, data):
        if not data.get("sura"):
            return Ayat.objects.none(), ""
        queryset = Ayat.objects.filter(sura=data.get("sura"))
        value = data.get("aya_start")

        if value not in queryset:
            value = queryset.first()

        return queryset, value

    def get_dynamic_aya_end_field(self, data):

        if not data.get("sura"):
            return Ayat.objects.none(), ""

        queryset = Ayat.objects.filter(sura=data.get("sura"))
        aya_end = data.get("aya_end")

        if aya_end not in queryset:
            aya_end = queryset.last()

        return queryset, aya_end

    def get_action_choices(self, request):
        choices = super(AyatTelawaAdmin, self).get_action_choices(request)
        choices.pop(0)
        choices.reverse()
        return choices


# @admin.register(Hadith)
# class HadithAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
#     fields = (
#         "text",
#         "text_without_tashkil",
#         "number",
#         "book",
#         "chapter",
#     )
# dynamic_fields = ("chapter",)

# def get_dynamic_chapter_field(self, data):
#     queryset = ChapterInAlSaheh.objects.filter(book=data.get("book"))
#     value = data.get("book")

#     if value not in queryset:
#         value = queryset.first()

#     return queryset, value


class TafsirHadithInAlSahehAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    form = HadithTafsirForm
    actions = [publish]
    list_filter = ["status"]
    fields = ("book", "chapter", "hadith", "text", "video_tafsir", "audio_tafsir", "video_url", "status")
    dynamic_fields = (
        "chapter",
        "hadith",
        "hadith__text_without_tashkil",
    )
    ordering = (
        "book",
        "chapter",
        "hadith",
    )

    def get_action_choices(self, request):
        choices = super(TafsirHadithInAlSahehAdmin, self).get_action_choices(request)
        choices.pop(0)
        choices.reverse()
        return choices

    def get_dynamic_chapter_field(self, data):
        queryset = ChapterInAlSaheh.objects.filter(book=data.get("book"))
        value = data.get("chapter")

        if value not in queryset:
            value = ""

        return queryset, value

    def get_dynamic_hadith_field(self, data):
        queryset = Hadith.objects.filter(book=data.get("book"), chapter=data.get("chapter"))
        value = data.get("hadith")
        # hadith_data = Hadith.objects.get(book=data.get("book"), chapter=data.get("chapter"))
        # hadith_data.text_without_tashkil = data.get("text")
        # hadith_data.save()
        hadith_data = queryset.first()
        hadith_data.text_without_tashkil = data.get("text")
        hadith_data.save()

        if value not in queryset:
            value = queryset.first()

        return queryset, value


admin.site.register(TafsirHadithInAlSaheh, TafsirHadithInAlSahehAdmin)


class BookAdmin(admin.ModelAdmin):
    exclude = ("size",)

    actions = [publish]
    list_filter = ["status", "type"]

    def get_action_choices(self, request):
        choices = super(BookAdmin, self).get_action_choices(request)
        choices.pop(0)
        choices.reverse()
        return choices


admin.site.register(Book, BookAdmin)


class BookSeachAdmin(admin.ModelAdmin):
    def get_action_choices(self, request):
        choices = super(BookSeachAdmin, self).get_action_choices(request)
        choices.pop(0)
        choices.reverse()
        return choices


admin.site.register(BookSeach, BookSeachAdmin)


class OtherScienceAdmin(admin.ModelAdmin):

    actions = [publish]
    list_filter = ["status"]

    def get_action_choices(self, request):
        choices = super(OtherScienceAdmin, self).get_action_choices(request)
        choices.pop(0)
        choices.reverse()
        return choices


admin.site.register(OtherScience, OtherScienceAdmin)


class OtherScienceSubjectAdmin(admin.ModelAdmin):

    actions = [publish]
    list_filter = ["status"]

    def get_action_choices(self, request):
        choices = super(OtherScienceSubjectAdmin, self).get_action_choices(request)
        choices.pop(0)
        choices.reverse()
        return choices


admin.site.register(OtherScienceSubject, OtherScienceSubjectAdmin)


class SessionsAdmin(DynamicModelAdminMixin, admin.ModelAdmin):

    actions = [publish]
    list_filter = [
        "type",
        "status",
        ("category", admin.EmptyFieldListFilter),
    ]
    fields = ("title", "type", "file", "video_url", "status", "category", "order_by")
    dynamic_fields = ("category",)

    def get_dynamic_category_field(self, data):
        queryset = ChapterInAlSaheh.objects.filter(book=data.get("type"))
        value = data.get("type")

        if value not in queryset:
            value = ""

        return queryset, value

    def get_action_choices(self, request):
        choices = super(SessionsAdmin, self).get_action_choices(request)
        choices.pop(0)
        choices.reverse()
        return choices


admin.site.register(Sessions, SessionsAdmin)


class SessionsCategoryAdmin(admin.ModelAdmin):

    # actions = [publish]
    # list_filter = ["status"]
    list_filter = [
        "type",
        ("order", admin.EmptyFieldListFilter),
    ]

    def get_action_choices(self, request):
        choices = super(SessionsCategoryAdmin, self).get_action_choices(request)
        choices.pop(0)
        choices.reverse()
        return choices


admin.site.register(SessionsCategory, SessionsCategoryAdmin)


class CallUsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(
        self,
        request,
        *args,
    ) -> bool:
        # return super().has_change_permission(request, obj)
        return False


admin.site.register(CallUs, CallUsAdmin)


#
class General_informationAdmin(admin.ModelAdmin):
    # exclude = ("visitor_count",)
    form = GeneralInfoForm

    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        else:
            return True


admin.site.register(General_information, General_informationAdmin)


@admin.register(BookInAlSaheh)
class BookInAlSahehAdmin(admin.ModelAdmin):
    pass


@admin.register(ChapterInAlSaheh)
class ChapterInAlSahehAdmin(admin.ModelAdmin):
    pass


@admin.register(Hadith)
class HadithAdmin(admin.ModelAdmin):
    pass


admin.site.register(Email)
admin.site.register(PhoneNumbers)

admin.site.register(RelatedSites)
admin.site.register(Ayat)