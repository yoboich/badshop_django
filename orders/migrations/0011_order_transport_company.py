# Generated by Django 4.2.5 on 2023-12-24 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_order_email_order_full_name_order_phone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='transport_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='orders.transportcompany', verbose_name='Транспортная компания'),
        ),
    ]
