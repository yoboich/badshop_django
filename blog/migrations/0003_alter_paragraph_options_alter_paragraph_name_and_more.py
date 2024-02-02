# Generated by Django 5.0 on 2024-02-01 12:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_paragraph'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paragraph',
            options={'verbose_name': 'Параграф', 'verbose_name_plural': 'Параграфы'},
        ),
        migrations.AlterField(
            model_name='paragraph',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='paragraph',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.paragraph', verbose_name='Родительский параграф'),
        ),
        migrations.AlterField(
            model_name='paragraph',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='Текст параграфа'),
        ),
    ]