# Generated by Django 4.1.4 on 2024-01-23 22:19

from django.db import migrations
import django_editorjs.fields


class Migration(migrations.Migration):

    dependencies = [
        ('social_platform', '0011_rename_content_post_body'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='body',
        ),
        migrations.AddField(
            model_name='post',
            name='content',
            field=django_editorjs.fields.EditorJsField(default='Content'),
            preserve_default=False,
        ),
    ]
