# Generated by Django 4.2.5 on 2023-12-23 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0032_alter_cart_session'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='seil_price',
        ),
    ]