# Generated by Django 5.1.1 on 2024-09-30 20:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_user_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='owner',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='own_listings', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
