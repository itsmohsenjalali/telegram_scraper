# Generated by Django 4.2.7 on 2023-11-06 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramgroup',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]
