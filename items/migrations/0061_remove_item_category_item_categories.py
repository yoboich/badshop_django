# Generated by Django 5.0 on 2024-02-13 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0060_alter_item_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='category',
        ),
        migrations.AddField(
            model_name='item',
            name='categories',
            field=models.ManyToManyField(blank=True, to='items.category', verbose_name='Категория'),
        ),
    ]