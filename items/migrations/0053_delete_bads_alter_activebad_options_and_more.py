# Generated by Django 5.0 on 2024-02-01 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0052_activebad_remove_item_active_bad_item_active_bads'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Bads',
        ),
        migrations.AlterModelOptions(
            name='activebad',
            options={'verbose_name': 'Действующее вещество', 'verbose_name_plural': 'Действующие вещества'},
        ),
        migrations.AlterField(
            model_name='item',
            name='active_bads',
            field=models.ManyToManyField(blank=True, to='items.activebad', verbose_name='Активное вещество'),
        ),
    ]
