# Generated by Django 4.1.4 on 2024-01-24 14:58

from django.db import migrations
import django_editorjs.fields


class Migration(migrations.Migration):

    dependencies = [
        ('social_platform', '0012_remove_post_body_post_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='content',
        ),
        migrations.AddField(
            model_name='post',
            name='data',
            field=django_editorjs.fields.EditorJsField(default='data'),
            preserve_default=False,
        ),
    ]
