# Generated by Django 4.2.5 on 2023-12-30 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_remove_payment_outer_id_order_outer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_response_id',
            field=models.CharField(blank=True, editable=False, max_length=255, null=True, verbose_name='айди платежа в банке'),
        ),
    ]
