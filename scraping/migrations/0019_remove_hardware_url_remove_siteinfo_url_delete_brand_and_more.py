# Generated by Django 4.0.4 on 2022-10-20 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0018_alter_siteinfo_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hardware',
            name='url',
        ),
        migrations.RemoveField(
            model_name='siteinfo',
            name='url',
        ),
        migrations.DeleteModel(
            name='Brand',
        ),
        migrations.DeleteModel(
            name='Hardware',
        ),
        migrations.DeleteModel(
            name='SiteInfo',
        ),
    ]
