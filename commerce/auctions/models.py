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
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}: \n" \
               f"title: {self.title}\n" \
               f"description: {self.description}\n" \
               f"starting bid: {self.starting_bid}\n" \
               f"category: {self.category}\n" \
               f"image_url: {self.image_url}\n" \
               f"active: {self.active}\n" \
               f"date created: {self.date_creation}"
