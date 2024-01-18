# Generated by Django 5.0 on 2024-01-16 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_orderitem_price_alter_orderitem_sale_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='promocode',
        ),
        migrations.AddField(
            model_name='order',
            name='promocode_discount',
            field=models.IntegerField(default=0, verbose_name='Скидка по промокоду'),
        ),
    ]