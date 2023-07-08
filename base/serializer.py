from rest_framework import serializers
from rest_framework.fields import CharField

from base.models import (
    Ayat,
    AyatTafsirAudio,
    AyatTafsirVideo,
    AyatTelawa,
    Book,
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
    RelatedSites,
    Sessions,
    SessionsCategory,
    Sura,
    TafsirHadithInAlSaheh, BookSeach
)

# fields = ['id', 'account_name', 'users', 'created']


class RelatedSitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedSites
        fields = "__all__"


class PhoneNumbersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumbers
        fields = "__all__"


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = "__all__"


class General_informationSerializer(serializers.ModelSerializer):
    about_sheikh_short = CharField()
    about_mousa_short = CharField()
    about_sheikh = CharField()
    about_mousa = CharField()

    class Meta:
        model = General_information
        fields = "__all__"


class CallUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallUs
        fields = "__all__"


class FatwaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fatwa
        fields = "__all__"

class ChapterSerializer(serializers.ModelSerializer):
    chapter_url = serializers.SerializerMethodField(read_only=True)

    def get_chapter_url(self, obj):
        page = obj.book.file.file.url + "#page" + str(obj.page)
        return page

    class Meta:
        model = BookSeach
        fields = ['key', 'chapter_url', 'page']


class BookSerializer(serializers.ModelSerializer):
    chapter = ChapterSerializer(many=True)
    class Meta:
        model = Book
        fields = "__all__"


class OtherScienceSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherScienceSubject
        fields = "__all__"


class OtherScienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherScience
        fields = "__all__"


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sessions
        fields = "__all__"


class SessionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionsCategory
        fields = "__all__"


class AyatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ayat
        fields = "__all__"


class AyatNameSerializer(serializers.ModelSerializer):
    sura = serializers.CharField(source='sura.name')

    class Meta:
        model = Ayat
        fields = "__all__"


class AyatTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ayat
        fields = ("text",)


class AyatTelawaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AyatTelawa
        fields = "__all__"


class AyatTafsirAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AyatTafsirAudio
        fields = "__all__"


class AyatTafsirVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AyatTafsirVideo
        fields = "__all__"


class SuraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sura
        fields = "__all__"


class SuraNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sura
        fields = ["name", "number"]


class TafsirHadithInAlSahehSerializer(serializers.ModelSerializer):
    class Meta:
        model = TafsirHadithInAlSaheh
        fields = "__all__"


class HadithSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hadith
        fields = "__all__"


class HadithNameSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source='book.name')
    class Meta:
        model = Hadith
        fields = "__all__"


class ChapterInAlSahehSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChapterInAlSaheh
        fields = "__all__"


class BookInAlSahehSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInAlSaheh
        fields = "__all__"


class DailyPublishSerializer(serializers.ModelSerializer):
    hadith = HadithSerializer()
    aya = AyatSerializer()

    class Meta:
        model = DailyPublish
        fields = "__all__"


class BookSeachSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSeach
        fields = "__all__"
