# Generated by Django 4.2.5 on 2023-09-07 09:54

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_alter_item_options_item_certificate_item_compound_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='certificate',
            field=models.ImageField(blank=True, null=True, upload_to='items/%Y/%m/%d/', verbose_name='Сертификаты'),
        ),
        migrations.AlterField(
            model_name='item',
            name='compound',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Состав товара'),
        ),
        migrations.AlterField(
            model_name='item',
            name='delivery',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Информация о доставке'),
        ),
        migrations.AlterField(
            model_name='item',
            name='discount',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Скидка'),
        ),
        migrations.AlterField(
            model_name='item',
            name='discount_price',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Цена со скидкой'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, unique='items/%Y/%m/%d/', upload_to='', verbose_name='Изображение товара'),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Название товара'),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Цена товара'),
        ),
        migrations.AlterField(
            model_name='item',
            name='rating',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Рэйтинг'),
        ),
        migrations.AlterField(
            model_name='item',
            name='text',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Описание товара'),
        ),
    ]
