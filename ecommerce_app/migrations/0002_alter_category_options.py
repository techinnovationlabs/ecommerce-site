# Generated by Django 3.2.5 on 2022-04-28 11:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('ecommerce_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]