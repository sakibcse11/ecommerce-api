# Generated by Django 5.2 on 2025-04-24 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='is_featured',
        ),
    ]
