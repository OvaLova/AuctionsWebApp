# Generated by Django 5.1.1 on 2024-10-05 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0024_listing_closed_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='item',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]
