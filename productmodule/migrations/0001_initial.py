# Generated by Django 5.1.7 on 2025-04-06 06:41

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('seller', models.UUIDField()),
                ('name', models.CharField(max_length=50)),
                ('brand_name', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('category', models.CharField(max_length=20)),
                ('cost_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image_paths', models.TextField(blank=True, null=True)),
                ('about_company_line1', models.CharField(max_length=500)),
                ('about_company_line2', models.CharField(blank=True, max_length=500, null=True)),
                ('about_company_line3', models.CharField(blank=True, max_length=500, null=True)),
                ('about_product_line1', models.CharField(max_length=500)),
                ('about_product_line2', models.CharField(blank=True, max_length=500, null=True)),
                ('about_product_line3', models.CharField(blank=True, max_length=500, null=True)),
                ('about_product_line4', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]
