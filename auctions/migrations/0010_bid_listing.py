# Generated by Django 5.1.1 on 2024-09-29 23:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_remove_listing_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid', to='auctions.listing'),
        ),
    ]
