# Generated by Django 5.0 on 2024-01-16 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0003_rename_seil_promocode_sale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promocode',
            name='sale',
        ),
        migrations.AddField(
            model_name='promocode',
            name='discount',
            field=models.IntegerField(default=0, verbose_name='Скидка в %'),
        ),
    ]
