# Generated by Django 3.1.3 on 2021-02-01 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('urls', '0003_auto_20210201_1637'),
    ]

    operations = [
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('http_code', models.IntegerField(verbose_name='Code reponse HTPP')),
                ('display_time', models.IntegerField(verbose_name="Temps d'affichage")),
                ('is_content_empty', models.BooleanField(blank=True, null=True, verbose_name='contenu de la réponse vide')),
                ('ssl_expiration_date', models.DateTimeField(blank=True, null=True, verbose_name="date d'expiration du certificat")),
                ('result', models.BooleanField(default=False, verbose_name='résultat global du test')),
                ('url', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='urls.url')),
            ],
            options={
                'verbose_name': 'Vérification',
                'verbose_name_plural': 'Vérifications',
            },
        ),
    ]
