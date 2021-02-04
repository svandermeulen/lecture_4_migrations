from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    starting_bid = models.FloatField()
    category = models.CharField(max_length=64)
    image_url = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}: title: {self.title}, description: {self.description}, starting bid: {self.starting_bid}, " \
               f"category: {self.category}, image_url: {self.image_url}, active: {self.active}"
