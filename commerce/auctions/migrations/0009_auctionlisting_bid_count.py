# Generated by Django 3.1.6 on 2021-02-05 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20210204_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='bid_count',
            field=models.IntegerField(default=0),
        ),
    ]
