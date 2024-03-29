# Generated by Django 4.2.5 on 2023-10-31 06:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0004_address'),
        ('items', '0017_alter_cartitem_options_cartitem_promocode'),
        ('orders', '0002_alter_appliedpromocode_options_alter_order_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderstatus',
            options={'verbose_name': 'Статусы заказов', 'verbose_name_plural': 'Статусы заказов'},
        ),
        migrations.AlterField(
            model_name='order',
            name='comment',
            field=models.CharField(blank=True, max_length=240, null=True, verbose_name='Комментарий к заказу'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.address', verbose_name='Адрес доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(blank=True, null=True, to='items.cartitem', verbose_name='Корзина'),
        ),
        migrations.AlterField(
            model_name='order',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sessions.session'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('OP', 'Оплачен'), ('DL', 'Доставлен'), ('NP', 'Не оплачен'), ('DD', 'Выполняется доставка')], default='NP', max_length=2, null=True, verbose_name='Статус заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.IntegerField(blank=True, null=True, verbose_name='Сумма заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
