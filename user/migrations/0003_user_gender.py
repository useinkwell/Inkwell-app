# Generated by Django 4.1.4 on 2023-03-30 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_user_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(default='gender-unassigned', max_length=20),
            preserve_default=False,
        ),
    ]
