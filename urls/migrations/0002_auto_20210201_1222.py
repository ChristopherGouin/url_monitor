# Generated by Django 3.1.3 on 2021-02-01 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urls', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='url',
            old_name='is_empty_content',
            new_name='is_content_empty',
        ),
    ]
