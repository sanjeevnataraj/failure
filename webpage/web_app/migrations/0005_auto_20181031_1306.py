# Generated by Django 2.1 on 2018-10-31 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0004_auto_20181031_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course_page',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
