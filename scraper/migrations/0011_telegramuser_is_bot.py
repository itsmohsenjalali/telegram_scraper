# Generated by Django 4.2.7 on 2023-11-08 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0010_telegramaccount_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='is_bot',
            field=models.BooleanField(default=False),
        ),
    ]
