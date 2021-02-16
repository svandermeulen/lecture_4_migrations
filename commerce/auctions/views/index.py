"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 15/02/2021
"""
from typing import Union, List

from django.contrib.auth.models import AnonymousUser
from django.db.models import QuerySet
from django.shortcuts import render

from ..models import AuctionListing, WatchList


def in_watchlist(request, listing: AuctionListing) -> bool:
    if isinstance(request.user, AnonymousUser):
        return False

    try:
        _ = WatchList.objects.get(user=request.user, listing=listing)
        return True
    except WatchList.DoesNotExist or TypeError:
        return False


def query_watchlist(request, listings: QuerySet) -> dict:
    return {listing.id: in_watchlist(request, listing=listing) for listing in listings}


def get_listings_context(request, listings: Union[QuerySet, List[AuctionListing]]) -> dict:
    watched = query_watchlist(request=request, listings=listings)
    return {
        "request": request,
        "listings": listings,
        "watched": watched
    }


def index(request):
    listings = AuctionListing.objects.filter(active=True)
    return render(request, "auctions/index.html", context=get_listings_context(request, listings=listings))


def main():
    pass


if __name__ == "__main__":
    main()
