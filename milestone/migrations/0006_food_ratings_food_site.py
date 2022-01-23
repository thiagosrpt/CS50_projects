# Generated by Django 4.0.1 on 2022-01-14 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('milestone', '0005_event_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='ratings',
            field=models.FloatField(default=None, max_length=3),
        ),
        migrations.AddField(
            model_name='food',
            name='site',
            field=models.CharField(default=None, max_length=255),
        ),
    ]