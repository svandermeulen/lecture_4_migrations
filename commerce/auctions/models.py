from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    starting_bid = models.FloatField()
    category = models.CharField(max_length=64)
    image_url = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    current_price = models.FloatField()
    bid_count = models.IntegerField(default=0)

    def get_bid_count(self):
        return Bid.objects.filter(listing=self).count()

    def save(self, *args, **kwargs):
        """
        Set the current price equal to the starting bid if no bids have been placed yet
        """
        if not self.current_price:
            self.current_price = self.starting_bid

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}: \n" \
               f"title: {self.title}\n" \
               f"description: {self.description}\n" \
               f"starting bid: {self.starting_bid}\n" \
               f"category: {self.category}\n" \
               f"image_url: {self.image_url}\n" \
               f"active: {self.active}\n" \
               f"date created: {self.date_creation}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    bid = models.FloatField()
    date_creation = models.DateTimeField(auto_now_add=True)
