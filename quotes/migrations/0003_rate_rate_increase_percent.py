# Generated by Django 4.2.6 on 2023-10-13 17:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quotes", "0002_coverage_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="rate",
            name="rate_increase_percent",
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=5),
            preserve_default=False,
        ),
    ]
