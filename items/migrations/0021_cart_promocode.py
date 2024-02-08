# Generated by Django 4.2.5 on 2023-10-31 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0001_initial'),
        ('items', '0020_remove_cart_promocode_alter_cart_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='promocode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='balance.promocode', verbose_name='Промокод'),
        ),
    ]
