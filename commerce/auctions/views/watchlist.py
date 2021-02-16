"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 15/02/2021
"""
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.db.models import QuerySet
from django.shortcuts import redirect, render

from ..decorators import login_required_message_and_redirect
from ..models import AuctionListing, WatchList
from .index import get_listings_context


def watch_list_view(request):
    watch_list = WatchList.objects.filter(user=request.user)

    if watch_list.first():
        listings = [wish.listing for wish in watch_list]
        return render(request, "auctions/watchlist.html", context=get_listings_context(request, listings=listings))
    messages.add_message(request, messages.INFO, "There are no items in your watchlist yet")
    return render(request, "auctions/watchlist.html")


@login_required_message_and_redirect(message="In order to add listings to your wishlist you should log in")
def add_to_watchlist(request, listing_id: int):
    listings = AuctionListing.objects.get(id=listing_id)

    watch_list = WatchList(
        user=request.user,
        listing=listings
    )
    watch_list.save()
    return redirect("auctions:watchlist")


def remove_from_watchlist(request, listing_id: int):
    listing = AuctionListing.objects.get(id=listing_id)
    watchlist = WatchList.objects.get(
        user=request.user,
        listing=listing
    )
    watchlist.delete()
    return redirect("auctions:index")





def main():
    pass


if __name__ == "__main__":
    main()
