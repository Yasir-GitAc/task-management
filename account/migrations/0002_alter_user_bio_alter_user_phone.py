# Generated by Django 4.2.7 on 2023-11-02 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, max_length=455, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
