# Generated by Django 5.0.4 on 2024-04-22 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm_app', '0008_inventory_delete_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='bought_products',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='products',
            field=models.CharField(max_length=175, null=True),
        ),
    ]