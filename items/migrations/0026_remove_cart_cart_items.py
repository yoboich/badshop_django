# Generated by Django 4.2.5 on 2023-11-18 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0025_cart_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='cart_items',
        ),
    ]
