"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 05/02/2021
"""
from .models import AuctionListing


class IdToListingTitle:
    regex = '.+'

    def to_python(self, value):
        listing = AuctionListing.objects.get(title=value)
        return int(listing.id)

    def to_url(self, value):

        listing = AuctionListing.objects.get(id=value)
        return listing.title


def main():
    pass


if __name__ == "__main__":
    main()
