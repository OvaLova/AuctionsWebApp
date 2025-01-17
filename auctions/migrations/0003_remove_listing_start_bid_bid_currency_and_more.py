# Generated by Django 5.1.1 on 2024-09-29 21:59

import auctions.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_listing_commment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='start_bid',
        ),
        migrations.AddField(
            model_name='bid',
            name='currency',
            field=models.CharField(choices=auctions.models.Bid.get_currencies, default='RON', max_length=3),
        ),
        migrations.AddField(
            model_name='bid',
            name='current_bid',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='bid',
            name='start_bid',
            field=models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(10)]),
        ),
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=auctions.models.Listing.get_category, default='Other', max_length=20),
        ),
        migrations.AddField(
            model_name='listing',
            name='photo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
