# Generated by Django 5.0 on 2024-04-14 18:17

import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_customuser_bonus_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='referral_code',
            field=models.CharField(blank=True, default=users.models.generate_referral_code, max_length=6, null=True, unique=True),
        ),
    ]
