# Generated by Django 3.2.4 on 2021-06-30 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20210630_0831'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='video_code',
            field=models.CharField(default='', max_length=15),
        ),
    ]
