# Generated by Django 5.1.1 on 2024-09-29 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_listing_start_bid_bid_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.TextField(max_length=2000),
        ),
    ]