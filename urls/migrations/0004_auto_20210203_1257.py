# Generated by Django 3.1.3 on 2021-02-03 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urls', '0003_auto_20210201_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='is_content_empty',
            field=models.BooleanField(verbose_name='la réponse doit-elle etre vide'),
        ),
    ]
