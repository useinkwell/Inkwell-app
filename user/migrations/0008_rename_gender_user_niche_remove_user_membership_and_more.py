# Generated by Django 4.1.4 on 2024-01-30 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_rename_invalidtoken_invalidaccesstoken'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='gender',
            new_name='niche',
        ),
        migrations.RemoveField(
            model_name='user',
            name='membership',
        ),
        migrations.AddField(
            model_name='user',
            name='is_pro_plan',
            field=models.BooleanField(default=False),
        ),
    ]
