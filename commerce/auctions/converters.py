"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 05/02/2021
"""
from .models import AuctionListing


class IdToListingTitle:
    # regex = '(?:\/[^\/]*)$'
    # regex = '.+'
    # regex = '((?<=\/)[^\/]+)$'  # Start from the end of the string and find all characters until the first backslash
    regex = "(?<=listing\/).+?(?=\/)|(?<=listing\/).+"

    def to_python(self, value):

        # if "/" in value:
        #     value = value.split("/")[0]

        listing = AuctionListing.objects.get(title=value)
        return int(listing.id)

    def to_url(self, value):
        listing = AuctionListing.objects.get(id=value)
        return listing.title


def main():
    pass


if __name__ == "__main__":
    main()
