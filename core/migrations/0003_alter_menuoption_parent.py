# Generated by Django 3.2.4 on 2021-06-19 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_menuoption_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuoption',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.menuoption'),
        ),
    ]
