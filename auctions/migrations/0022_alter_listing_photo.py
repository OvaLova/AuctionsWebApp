# Generated by Django 5.1.1 on 2024-10-05 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0021_alter_bid_start_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='photo',
            field=models.ImageField(blank=True, upload_to='listings/'),
        ),
    ]
