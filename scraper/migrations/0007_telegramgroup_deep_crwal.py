# Generated by Django 4.2.7 on 2023-11-07 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0006_alter_telegramuser_first_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramgroup',
            name='deep_crwal',
            field=models.BooleanField(default=False),
        ),
    ]