# Generated by Django 3.2.5 on 2022-05-18 07:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ('ecommerce_app', '0038_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(db_index=True, default=uuid.uuid4, editable=False, max_length=50, unique=True),
        ),
    ]
