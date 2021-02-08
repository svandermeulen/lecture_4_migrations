from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse


from .decorators import login_required_message_and_redirect
from .forms import NewListingForm, NewBidForm
from .models import User, AuctionListing, Bid




def index(request):
    listings_active = AuctionListing.objects.filter(active=True)
    context = {"listings": listings_active}
    return render(request, "auctions/index.html", context=context)


def my_listings_view(request):
    listings_user = AuctionListing.objects.filter(user=request.user)
    context = {"listings": listings_user}
    return render(request, "auctions/my_listings.html", context=context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            next_page = request.POST.get('next')
            if next_page:
                return HttpResponseRedirect(next_page)
            return redirect("auctions:index")

        else:

            messages.add_message(request, messages.ERROR, "Invalid username and/or password.")
            return render(request, "auctions/login.html")
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
            messages.add_message(request, messages.ERROR, "Passwords must match.")
            return render(request, "auctions/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.add_message(request, messages.ERROR, "Username already taken.")
            return render(request, "auctions/register.html")
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


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


def listing_view(request, listing_id: int):
    context = {
        "listing": AuctionListing.objects.get(id=listing_id),
        "form": NewBidForm()
    }
    return render(request, "auctions/listing.html", context=context)


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


def close_listing_view(request, listing_id: int):
    """
    Close the auction
    """
    listing = AuctionListing.objects.get(id=listing_id)
    listing.active = False
    listing.save()
    return redirect("auctions:index")


def reopen_listing_view(request, listing_id: int):
    """
    Reopen a closed auction
    """
    listing = AuctionListing.objects.get(id=listing_id)
    listing.active = True
    listing.save()
    return redirect("auctions:index")


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
