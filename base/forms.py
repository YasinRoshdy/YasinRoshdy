# from django import forms
# from django.db import models

# from base.models import DailyPublish


# class DailyGroupForm(forms.ModelForm):

#     hadeath = forms.CharField()
#     aya = forms.CharField()
#     fatwa = forms.CharField()
#     part_of_book = forms.CharField()

#     date = models.DateField(auto_now=False, auto_now_add=False)

#     def save(self, commit=True):
#         hadeath = self.cleaned_data.get("hadeath", None)
#         aya = self.cleaned_data.get("aya", None)
#         fatwa = self.cleaned_data.get("fatwa", None)
#         part_of_book = self.cleaned_data.get("part_of_book", None)
#         date = self.cleaned_data.get("date", None)

#         # super(DailyGroupForm, self).save(commit=commit)
#         if hadeath is not None:
#             obj = DailyPublish(publish_type="hadeth", content=hadeath, date=date)
#             obj.save()
#         if aya is not None:
#             obj = DailyPublish(publish_type="aya", content=aya, date=date)
#             obj.save()
#         if fatwa is not None:
#             obj = DailyPublish(publish_type="fatwa", content=fatwa, date=date)
#             obj.save()
#         if part_of_book is not None:
#             obj = DailyPublish(publish_type="part_of_book", content=part_of_book, date=date)
#             obj.save()
#         return

#     class Meta:
#         model = DailyPublish
#         fields = "__all__"
# from django import forms

# from base.models import Fatwa


# class FatwaModelForm(forms.ModelForm):
#     answer_text = forms.CharField(
#         widget=forms.Textarea(attrs={"class": "form-control", "dir": "rtl", "placeholder": "الفتوي"}),
#     )

#     class Meta:
#         model = Fatwa
#         fields = "__all__"


# from django import forms

# from base.models import AyatTafsir, CallUs


# class CallUsForm(forms.ModelForm):
#     message = forms.CharField(
#         widget=forms.Textarea(attrs={"dir": "rtl", "placeholder": "الرسال", "verbose_name": "verbose_name"}),
#     )

#     class Meta:
#         model = CallUs
#         fields = "__all__"


# class AyatTafsirdminForm(forms.ModelForm):
#     class Meta:
#         model = AyatTafsir
#         fields = "__all__"
#         widgets = {
#             "aya_start": forms.widgets.Select(choices=[("1", "1"), ("2", "2"), ("3", "3")]),
#         }


from django import forms

from base.models import AyatTafsirAudio, AyatTafsirVideo, Book, General_information, TafsirHadithInAlSaheh

from django.utils.translation import gettext as _


class GeneralInfoForm(forms.ModelForm):
    about_sheikh_short = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "5", "required": False}), label=_("about_sheikh_short"), required=False
    )
    about_mousa_short = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "5", "required": False}), label=_("about_mousa_short"), required=False
    )
    # about_sheikh = forms.CharField(widget=forms.Textarea(attrs={"rows": "7", "required": False}), label=_("about_sheikh"), required=False)
    # about_mousa = forms.CharField(widget=forms.Textarea(attrs={"rows": "7", "required": False}), label=_("about_mousa"), required=False)
    privacy_policy = forms.CharField(widget=forms.Textarea(attrs={"rows": "7", "required": False}), label=_("privacy policy"), required=False)

    class Meta:
        model = General_information
        fields = "__all__"


class AyatTafsirVideoForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={"rows": "5", "required": False}), label=_("tafsir_ayat_text"), required=False)
    video_url = forms.CharField()

    class Meta:
        model = AyatTafsirVideo
        fields = "__all__"


class AyatTafsirAudioForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={"rows": "5", "required": False}), label=_("tafsir_ayat_text"), required=False)

    class Meta:
        model = AyatTafsirAudio
        fields = "__all__"


class HadithTafsirForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={"rows": "5", "required": False}), label=_("tafsir_hadith_text"), required=False)

    class Meta:
        model = TafsirHadithInAlSaheh
        fields = "__all__"


class BooksForms(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ("page_count",)
