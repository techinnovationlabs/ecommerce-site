# Generated by Django 3.2.5 on 2022-05-19 06:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ecommerce_app', '0064_auto_20220519_0614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
