"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 15/02/2021
"""
from django.contrib import messages
from django.shortcuts import redirect, render

from ..decorators import login_required_message_and_redirect
from ..forms import NewBidForm
from ..models import AuctionListing, Bid
from ..views.index import get_listings_context


def my_biddings_view(request):
    bidding_list = Bid.objects.filter(user=request.user)
    if bidding_list.first():
        listings = list({bidding.listing for bidding in bidding_list})
        return render(request, "auctions/biddings.html", context=get_listings_context(request, listings=listings))


@login_required_message_and_redirect(message="In order to place a bid you should be logged in")
def place_bid(request, listing_id: int):
    listing = AuctionListing.objects.get(id=listing_id)
    if request.method == "POST":

        form = NewBidForm(request.POST)
        if form.is_valid():

            bid_value = form.cleaned_data["bid"]

            if bid_value <= listing.current_price:
                messages.add_message(
                    request,
                    messages.ERROR, f'Your bid should be higher than the current price {listing.current_price}'
                )

                return redirect("auctions:listing", listing=listing.title)

            # Create new entry in the Bid table
            bid = Bid(
                bid=bid_value,
                user=request.user,
                listing=listing
            )
            bid.save()

            # Change the price in the AuctionListing table
            listing.current_price = bid.bid
            listing.save()
            return redirect("auctions:index")

    return redirect("auctions:listing", listing_id=listing.id)


def main():
    pass


if __name__ == "__main__":
    main()
