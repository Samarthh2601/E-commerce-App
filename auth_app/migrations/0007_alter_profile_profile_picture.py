# Generated by Django 5.0.4 on 2024-04-09 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0006_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='profile_pics'),
        ),
    ]
