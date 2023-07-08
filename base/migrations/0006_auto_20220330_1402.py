# Generated by Django 3.2.12 on 2022-03-30 12:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.file
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('base', '0005_alter_sessions_video_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ayat',
            name='sura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.sura', verbose_name='سورة'),
        ),
        migrations.AlterField(
            model_name='ayattafsiraudio',
            name='aya_end',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='AyatTafsirAudioaya_end', to='base.ayat', verbose_name='نهاية تفسير الأيات آية رقم'),
        ),
        migrations.AlterField(
            model_name='ayattafsiraudio',
            name='aya_start',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='AyatTafsirAudioaya_start', to='base.ayat', verbose_name='بدايه تفسير الأيات من آية رقم'),
        ),
        migrations.AlterField(
            model_name='ayattafsiraudio',
            name='sound_tafsir',
            field=filer.fields.file.FilerFileField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sound_tafsir_file', to='filer.file', verbose_name='التفسير الصوتي'),
        ),
        migrations.AlterField(
            model_name='ayattafsiraudio',
            name='sura',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='base.sura', verbose_name='سورة'),
        ),
        migrations.AlterField(
            model_name='ayattafsirvideo',
            name='aya_end',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='AyatTafsirVideoaya_end', to='base.ayat', verbose_name='نهاية تفسير الأيات آية رقم'),
        ),
        migrations.AlterField(
            model_name='ayattafsirvideo',
            name='aya_start',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='AyatTafsirVideoaya_start', to='base.ayat', verbose_name='بدايه تفسير الأيات من آية رقم'),
        ),
        migrations.AlterField(
            model_name='ayattafsirvideo',
            name='sura',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='base.sura', verbose_name='سورة'),
        ),
        migrations.AlterField(
            model_name='ayattafsirvideo',
            name='video_tafsir',
            field=filer.fields.file.FilerFileField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='video_tafsir_fileAyatTafsirVideo', to='filer.file', verbose_name='ملف التفسير المرئي'),
        ),
        migrations.AlterField(
            model_name='ayattelawa',
            name='aya_end',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='AyatTelawaaya_end', to='base.ayat', verbose_name='نهاية تفسير الأيات آية رقم'),
        ),
        migrations.AlterField(
            model_name='ayattelawa',
            name='aya_start',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='AyatTelawaaya_start', to='base.ayat', verbose_name='بدايه تفسير الأيات من آية رقم'),
        ),
        migrations.AlterField(
            model_name='ayattelawa',
            name='sura',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='base.sura', verbose_name='سورة'),
        ),
        migrations.AlterField(
            model_name='ayattelawa',
            name='telawa',
            field=filer.fields.file.FilerFileField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='telawa_file', to='filer.file', verbose_name='التلاوة'),
        ),
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='book_covers', to=settings.FILER_IMAGE_MODEL, verbose_name='الصوره'),
        ),
        migrations.AlterField(
            model_name='book',
            name='file',
            field=filer.fields.file.FilerFileField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='filer.file', verbose_name='الملف'),
        ),
        migrations.AlterField(
            model_name='chapterinalsaheh',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.bookinalsaheh', verbose_name='كتاب في صحيح البخاري'),
        ),
        migrations.AlterField(
            model_name='dailypublish',
            name='aya',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='base.ayat', verbose_name=' أيات'),
        ),
        migrations.AlterField(
            model_name='dailypublish',
            name='book_in_alsaheh',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='base.bookinalsaheh', verbose_name='الكتب/صحيح البخاري'),
        ),
        migrations.AlterField(
            model_name='dailypublish',
            name='chapter_in_alsaheh',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='base.chapterinalsaheh', verbose_name='الباب/صحيح البخاري'),
        ),
        migrations.AlterField(
            model_name='dailypublish',
            name='hadith',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='base.hadith', verbose_name='حديث'),
        ),
        migrations.AlterField(
            model_name='dailypublish',
            name='sura',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='base.sura', verbose_name='سورة'),
        ),
        migrations.AlterField(
            model_name='fatwa',
            name='file',
            field=filer.fields.file.FilerFileField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='filer.file', verbose_name='الملف'),
        ),
        migrations.AlterField(
            model_name='general_information',
            name='cover_page',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cover_page', to=settings.FILER_IMAGE_MODEL, verbose_name=' صوره  cover حجم الصورة المثالي  الطول:310px - العرض:1440px'),
        ),
        migrations.AlterField(
            model_name='general_information',
            name='mousa_img',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='mousa_img', to=settings.FILER_IMAGE_MODEL, verbose_name='صورة الجمعية في  صفحة بنذة عنا'),
        ),
        migrations.AlterField(
            model_name='general_information',
            name='sheikh_img',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sheikh_img', to=settings.FILER_IMAGE_MODEL, verbose_name='صورة الشيخ في  صفحة بنذة عنا '),
        ),
        migrations.AlterField(
            model_name='hadith',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.bookinalsaheh', verbose_name='كتاب في صحيح البخاري'),
        ),
        migrations.AlterField(
            model_name='hadith',
            name='chapter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.chapterinalsaheh', verbose_name='الباب/صحيح البخاري'),
        ),
        migrations.AlterField(
            model_name='otherscience',
            name='file',
            field=filer.fields.file.FilerFileField(on_delete=django.db.models.deletion.PROTECT, to='filer.file', verbose_name='محتوي'),
        ),
        migrations.AlterField(
            model_name='otherscience',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.othersciencesubject', verbose_name='مواضيع العلوم الأخري'),
        ),
        migrations.AlterField(
            model_name='sessions',
            name='file',
            field=filer.fields.file.FilerFileField(on_delete=django.db.models.deletion.PROTECT, to='filer.file', verbose_name='المحتوي'),
        ),
        migrations.AlterField(
            model_name='tafsirhadithinalsaheh',
            name='audio_tafsir',
            field=filer.fields.file.FilerFileField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='audio_hadith_file', to='filer.file', verbose_name='التفسير الصوتي'),
        ),
        migrations.AlterField(
            model_name='tafsirhadithinalsaheh',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.bookinalsaheh', verbose_name='كتاب في صحيح البخاري'),
        ),
        migrations.AlterField(
            model_name='tafsirhadithinalsaheh',
            name='chapter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.chapterinalsaheh', verbose_name='الباب/صحيح البخاري'),
        ),
        migrations.AlterField(
            model_name='tafsirhadithinalsaheh',
            name='hadith',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.hadith', verbose_name='حديث'),
        ),
        migrations.AlterField(
            model_name='tafsirhadithinalsaheh',
            name='video_tafsir',
            field=filer.fields.file.FilerFileField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='TafsirHadithInAlSahehvideo_tafsir_file', to='filer.file', verbose_name='التفسير المرئي'),
        ),
    ]
