# Generated by Django 5.1.1 on 2024-10-05 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_alter_listing_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='photo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]