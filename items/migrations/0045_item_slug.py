# Generated by Django 5.0 on 2024-02-01 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0044_bads_alter_certificateimages_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(blank=True, default='', help_text='Оставьте пустым, оно само генерируется при заполнении названия', null=True, verbose_name='Слаг'),
        ),
    ]
