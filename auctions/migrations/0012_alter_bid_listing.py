# Generated by Django 5.1.1 on 2024-09-30 16:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_commment_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='listing',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid', to='auctions.listing'),
        ),
    ]
