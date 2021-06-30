# Generated by Django 3.2.4 on 2021-06-30 05:31

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_favorite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='exercises',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='remarks',
        ),
        migrations.RemoveField(
            model_name='exercise',
            name='youtube_code',
        ),
        migrations.AddField(
            model_name='exercise',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
