# Generated by Django 3.1.6 on 2021-05-05 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mentalcheck', '0005_auto_20210505_1819'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questiontext',
            old_name='date',
            new_name='date_answered',
        ),
    ]