# Generated by Django 5.0 on 2024-04-14 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0005_alter_slidertop_image_alter_slidertwo_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='slidertop',
            name='link',
            field=models.CharField(blank=True, max_length=299, null=True),
        ),
        migrations.AddField(
            model_name='slidertwo',
            name='link',
            field=models.CharField(blank=True, max_length=299, null=True),
        ),
    ]
