# Generated by Django 3.1.6 on 2021-02-04 19:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auctionlisting_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]