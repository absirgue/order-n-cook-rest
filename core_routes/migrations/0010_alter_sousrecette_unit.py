# Generated by Django 4.1.7 on 2023-04-24 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_routes', '0009_remove_sousrecette_quantity_in_kilogramme_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sousrecette',
            name='unit',
            field=models.CharField(default='kilogramme', max_length=100),
        ),
    ]
