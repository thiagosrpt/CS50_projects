# Generated by Django 4.0.1 on 2022-01-13 03:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('milestone', '0003_rename_likes_like'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='created',
            new_name='timestamp',
        ),
        migrations.RenameField(
            model_name='food',
            old_name='created',
            new_name='timestamp',
        ),
        migrations.RenameField(
            model_name='like',
            old_name='created',
            new_name='timestamp',
        ),
    ]
