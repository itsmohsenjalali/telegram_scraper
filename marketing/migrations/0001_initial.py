# Generated by Django 4.2.7 on 2023-11-08 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('scraper', '0007_telegramgroup_deep_crwal'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketingPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('start_date', models.DateTimeField()),
                ('strategy', models.CharField(choices=[('iug', 'Add User'), ('smu', 'Send Message To User'), ('full', 'Add User and Send Message')], max_length=4)),
                ('message', models.TextField(blank=True, null=True)),
                ('selected_group', models.ManyToManyField(related_name='marketing_plan', to='scraper.telegramgroup')),
            ],
        ),
    ]