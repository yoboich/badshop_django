# Generated by Django 5.0 on 2024-02-13 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0053_delete_bads_alter_activebad_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, default='', help_text='Оставьте пустым, оно само генерируется при заполнении названия', max_length=500, null=True, verbose_name='Слаг'),
        ),
    ]