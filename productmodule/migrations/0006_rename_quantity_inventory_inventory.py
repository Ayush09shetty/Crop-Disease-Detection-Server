# Generated by Django 5.2 on 2025-04-14 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productmodule', '0005_inventory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventory',
            old_name='quantity',
            new_name='inventory',
        ),
    ]
