# Generated by Django 5.2 on 2025-04-24 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_options_user_first_name_user_last_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-date_joined'], 'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
    ]
