# Generated by Django 4.0.4 on 2022-10-17 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0012_alter_siteinfo_price_alter_siteinfo_product_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteinfo',
            name='price',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='siteinfo',
            name='product_point',
            field=models.TextField(),
        ),
    ]
