# Generated by Django 3.1.3 on 2021-02-01 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urls', '0002_auto_20210201_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='is_content_empty',
            field=models.BooleanField(verbose_name='la réponse doit-elle contenir du text ?'),
        ),
        migrations.AlterField(
            model_name='url',
            name='ssl_expiration',
            field=models.IntegerField(blank=True, help_text='Le test sera ok si le certificat ssl expire dans plus de jours que cette durée. Laisser vide pour ne pas tester', null=True, verbose_name="Durée minimal d'expiration (jours)"),
        ),
        migrations.DeleteModel(
            name='UrlsTest',
        ),
    ]
