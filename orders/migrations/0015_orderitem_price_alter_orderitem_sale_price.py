# Generated by Django 5.0 on 2024-01-16 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_rename_price_orderitem_sale_price_order_promocode'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='sale_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]