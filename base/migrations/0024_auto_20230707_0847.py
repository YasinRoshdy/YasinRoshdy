# Generated by Django 3.2.12 on 2023-07-07 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0023_auto_20230622_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinalsaheh',
            name='active_flag',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='bookinalsaheh',
            name='order_by',
            field=models.IntegerField(default=1, verbose_name='ترتيب'),
        ),
        migrations.AddField(
            model_name='otherscience',
            name='order_by',
            field=models.IntegerField(default=1, verbose_name='ترتيب'),
        ),
        migrations.AddField(
            model_name='sessions',
            name='order_by',
            field=models.IntegerField(default=1, verbose_name='ترتيب'),
        ),
        migrations.AddField(
            model_name='sessionscategory',
            name='active_flag',
            field=models.BooleanField(default=True, verbose_name='active flag'),
        ),
        migrations.AlterField(
            model_name='othersciencesubject',
            name='order',
            field=models.IntegerField(null=True, verbose_name='ترتيب'),
        ),
        migrations.AlterUniqueTogether(
            name='dailypublish',
            unique_together=set(),
        ),
    ]