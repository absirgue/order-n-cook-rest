# Generated by Django 4.1.7 on 2023-06-07 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_routes', '0005_alter_recette_last_selling_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recette',
            name='last_selling_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
