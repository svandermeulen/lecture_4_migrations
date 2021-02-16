"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 15/02/2021
"""
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from ..forms import NewListingForm, NewBidForm
from ..models import AuctionListing, Comment
from .index import get_listings_context


def listing_view(request, listing_id: int):
    listing = AuctionListing.objects.get(id=listing_id)
    comments = Comment.objects.filter(listing=listing)
    context = {
        "listing": listing,
        "form": NewBidForm(),
        "comments": comments
    }
    return render(request, "auctions/listing.html", context=context)


def my_listings_view(request):
    listings = AuctionListing.objects.filter(user=request.user)
    return render(request, "auctions/my_listings.html", context=get_listings_context(request, listings=listings))


def create_listing_view(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():

            if request.POST.get("Save"):
                listing = AuctionListing(
                    user=request.user,
                    title=form.cleaned_data["title"],
                    description=form.cleaned_data["description"],
                    starting_bid=form.cleaned_data["starting_bid"],
                    category=form.cleaned_data["category"],
                    image_url=form.cleaned_data["image_url"],
                    current_price=form.cleaned_data["starting_bid"]
                )
                listing.save()
                return redirect("auctions:index")
            elif request.POST.get("Overwrite"):
                listing = AuctionListing.objects.get(id=request.POST.get("listing_id"))
                listing.title = form.cleaned_data["title"]
                listing.description = form.cleaned_data["description"]
                listing.starting_bid = form.cleaned_data["starting_bid"]
                listing.category = form.cleaned_data["category"]
                listing.image_url = form.cleaned_data["image_url"]
                listing.save()
                return redirect("auctions:index")

        messages.add_message(request, messages.ERROR, "Input is invalid.")
        return render(request, "auctions/create.html", {
            "form": form,
        })

    context = {"form": NewListingForm()}
    return render(request, "auctions/create.html", context)


def edit_listing_view(request, listing_id: int):
    listing = AuctionListing.objects.get(id=listing_id)

    form = NewListingForm(
        initial={
            "title": listing.title,
            "description": listing.description,
            "starting_bid": listing.starting_bid,
            "category": listing.category,
            "image_url": listing.image_url
        }
    )

    if listing.starting_bid != listing.current_price:
        form.fields["starting_bid"].widget.attrs["read_only"] = True
        form.fields["starting_bid"].widget = form.fields["starting_bid"].hidden_widget()

    context = {
        "form": form,
        "listing_id": listing.id
    }
    return render(request, "auctions/create.html", context)


def change_listing_activty_view(request, listing_id: int):
    """
    Open/close the auction of a listing
    """
    listing = AuctionListing.objects.get(id=listing_id)
    listing.active = not listing.active
    listing.save()
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)


def main():
    pass


if __name__ == "__main__":
    main()
