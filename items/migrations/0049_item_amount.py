# Generated by Django 5.0 on 2024-02-01 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0048_item_vendor_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='amount',
            field=models.IntegerField(default=0, verbose_name='Остаток на складе'),
        ),
    ]