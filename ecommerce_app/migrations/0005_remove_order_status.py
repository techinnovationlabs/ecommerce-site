# Generated by Django 3.2.5 on 2022-05-07 12:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('ecommerce_app', '0004_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
    ]
