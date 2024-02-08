# Generated by Django 4.2.5 on 2023-12-21 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        ('items', '0030_alter_favoriteitem_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='sessions.session'),
        ),
        migrations.AlterField(
            model_name='favoriteitem',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sessions.session'),
        ),
    ]
