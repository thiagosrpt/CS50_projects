# Generated by Django 3.2.5 on 2021-08-09 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20210804_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.TextField(blank=True, max_length=1280),
        ),
        migrations.AlterField(
            model_name='listing',
            name='photo',
            field=models.CharField(blank=True, max_length=1280),
        ),
    ]
