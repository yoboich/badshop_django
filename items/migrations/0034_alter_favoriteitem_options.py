# Generated by Django 4.2.5 on 2023-12-24 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0033_remove_item_seil_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favoriteitem',
            options={'verbose_name': 'Избранный товар', 'verbose_name_plural': 'Избранные товары'},
        ),
    ]
