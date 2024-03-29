# Generated by Django 5.0 on 2024-02-01 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0045_item_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(blank=True, default='', help_text='Оставьте пустым, оно само генерируется при заполнении названия', max_length=500, null=True, verbose_name='Слаг'),
        ),
    ]
