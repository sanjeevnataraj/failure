# Generated by Django 2.1 on 2018-11-21 12:51

from django.db import migrations
import froala_editor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0006_college_detail_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='streams',
            name='about_exam',
            field=froala_editor.fields.FroalaField(blank=True, max_length=2, null=True),
        ),
    ]
