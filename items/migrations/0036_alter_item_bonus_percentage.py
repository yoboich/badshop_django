# Generated by Django 5.0 on 2024-01-12 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0035_remove_cart_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='bonus_percentage',
            field=models.FloatField(blank=True, default=15, null=True, verbose_name='Процент бонусных баллов'),
        ),
    ]
