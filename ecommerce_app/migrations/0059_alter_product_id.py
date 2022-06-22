# Generated by Django 3.2.5 on 2022-05-19 04:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ('ecommerce_app', '0058_remove_order_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]