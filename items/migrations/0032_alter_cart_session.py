# Generated by Django 4.2.5 on 2023-12-21 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        ('items', '0031_alter_cart_session_alter_favoriteitem_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sessions.session'),
        ),
    ]
