# Generated by Django 4.1.7 on 2023-04-26 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_routes', '0013_alter_recette_duration_alter_recette_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recette',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
