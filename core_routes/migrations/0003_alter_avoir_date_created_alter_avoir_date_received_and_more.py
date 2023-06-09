# Generated by Django 4.1.7 on 2023-07-03 12:44

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_routes', '0002_avoiritem_quantity_received_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avoir',
            name='date_created',
            field=models.DateField(default=datetime.date.today, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date(2023, 7, 3), message='Date can not be later than today')]),
        ),
        migrations.AlterField(
            model_name='avoir',
            name='date_received',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date(2023, 7, 3), message='Date can not be later than today')]),
        ),
        migrations.AlterField(
            model_name='bonlivraison',
            name='date_created',
            field=models.DateField(default=datetime.date.today, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date(2023, 7, 3), message='Date can not be later than today')]),
        ),
        migrations.AlterField(
            model_name='commande',
            name='date_created',
            field=models.DateField(default=datetime.date.today, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date(2023, 7, 3), message='Date can not be later than today')]),
        ),
        migrations.AlterField(
            model_name='commande',
            name='expected_delivery_date',
            field=models.DateField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(limit_value=datetime.date(2023, 7, 3), message='Date can not be later than today')]),
        ),
        migrations.AlterField(
            model_name='commandeitem',
            name='received_avoir',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='fournisseurback',
            name='created_on',
            field=models.DateField(default=datetime.date.today, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date(2023, 7, 3), message='Date can not be later than today')]),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date_created',
            field=models.DateField(default=datetime.date.today, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date(2023, 7, 3), message='Date can not be later than today')]),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_taxes',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(limit_value=0)]),
        ),
        migrations.AlterField(
            model_name='produitback',
            name='created_on',
            field=models.DateField(default=datetime.date.today, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date(2023, 7, 3), message='Date can not be later than today')]),
        ),
        migrations.AlterField(
            model_name='produitpricetracker',
            name='created_on',
            field=models.DateField(default=datetime.date.today, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date(2023, 7, 3), message='Date can not be later than today')]),
        ),
        migrations.AlterField(
            model_name='recette',
            name='last_modification',
            field=models.DateField(default=datetime.date.today, validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date(2023, 7, 3), message='Date can not be later than today')]),
        ),
    ]
