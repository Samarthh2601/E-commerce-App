# Generated by Django 5.0.4 on 2024-04-19 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm_app', '0005_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='user',
        ),
    ]
