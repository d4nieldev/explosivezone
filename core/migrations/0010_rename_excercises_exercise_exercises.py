# Generated by Django 3.2.4 on 2021-06-20 00:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20210620_0011'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exercise',
            old_name='excercises',
            new_name='exercises',
        ),
    ]