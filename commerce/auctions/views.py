from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import NewListingForm, NewBidForm
from .models import User, AuctionListing, Bid


def index(request):

    listings_active = AuctionListing.objects.filter(active=True)
    context = {"listings": listings_active}
    return render(request, "auctions/index.html", context=context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("auctions:index")
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


def create_listing_view(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
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
        return render(request, "auctions/create.html", {
            "form": form,
            "message": "Input is invalid"
        })

    context = {"form": NewListingForm()}
    return render(request, "auctions/create.html", context)


def listing_view(request, listing: str):
    context = {
        "listing": AuctionListing.objects.get(title=listing),
        "form": NewBidForm()
    }
    return render(request, "auctions/listing.html", context=context)


def place_bid(request, listing_id: int):
    listing = AuctionListing.objects.get(id=listing_id)
    if request.method == "POST":

        form = NewBidForm(request.POST)
        if form.is_valid():

            # Create new entry in the Bid table
            bid = Bid(
                bid=form.cleaned_data["bid"],
                user=request.user,
                listing=listing
            )
            bid.save()

            # Change the price in the AuctionListing table
            listing.current_price = bid.bid
            listing.save()
            return redirect("auctions:index")

    return redirect("auctions:listing", listing=listing.title)
