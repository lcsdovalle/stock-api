# Generated by Django 4.2 on 2023-12-22 23:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0001_initial"),
        ("stock", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stock",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="product.product",
                unique=True,
            ),
        ),
    ]
