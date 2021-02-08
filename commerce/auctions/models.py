import logging

from django.contrib.auth.models import AbstractUser
from django.db import models


logger = logging.getLogger(__name__)


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

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.current_price = self.get_current_price()

    def get_latest_bid(self):
        return Bid.objects.filter(listing=self).latest("date_creation")

    def get_bid_count(self):
        return Bid.objects.filter(listing=self).count()

    def get_current_price(self):
        """
        Return the latest bid
        Return the starting bid if no bids have been placed yet
        """

        try:
            return Bid.objects.filter(listing=self).latest("date_creation").bid
        except Bid.DoesNotExist:
            logger.debug(f"No bids have been placed yet, taking starting bid instead")
            return self.starting_bid

    def __str__(self):
        return f"{self.id}: {self.title}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    bid = models.FloatField()
    date_creation = models.DateTimeField(auto_now_add=True)
