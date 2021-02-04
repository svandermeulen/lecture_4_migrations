from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    user = models.CharField(max_length=255)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    starting_bid = models.FloatField()
    category = models.CharField(max_length=64)
    image_url = models.CharField(max_length=255)