# Generated by Django 3.1.3 on 2021-02-01 12:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nom du site')),
                ('url', models.URLField(verbose_name='Url à controler')),
                ('description', models.TextField(blank=True, max_length=250, null=True, verbose_name='Description')),
                ('http_code', models.IntegerField(blank=True, help_text='Laisser vide pour ne pas tester', null=True, verbose_name='Code de réponse HTTP attendu')),
                ('display_time', models.IntegerField(blank=True, help_text='Laisser vide pour ne pas tester', null=True, verbose_name="Temps d'affichage maximum attendu (ms)")),
                ('is_empty_content', models.BooleanField(verbose_name='la réponse doit-elle contenir du text')),
                ('ssl_expiration', models.IntegerField(blank=True, help_text='Le test sera ok le certificat ssl expire dans plus de jours que cette durée. Laisser vide pour ne pas tester', null=True, verbose_name="Durée minimal d'expiration (jours)")),
                ('is_auto_check', models.BooleanField(default=True, help_text='la vérification sera lancée par le script', verbose_name='Vérification automatique')),
                ('is_mail_report', models.BooleanField(default=False, verbose_name='Rapport par mail')),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Url',
                'verbose_name_plural': 'Urls',
            },
        ),
        migrations.CreateModel(
            name='UrlsTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('http_code', models.IntegerField(verbose_name='Code reponse HTPP')),
                ('display_time', models.IntegerField(verbose_name="Temps d'affichage")),
                ('is_content_empty', models.BooleanField(blank=True, null=True, verbose_name='contenu de la réponse vide')),
                ('ssl_expiration_date', models.DateTimeField(blank=True, null=True, verbose_name="date d'expiration du certificat")),
                ('url', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='urls.url')),
            ],
            options={
                'verbose_name': 'Test',
                'verbose_name_plural': 'Tests',
            },
        ),
    ]
