from typing import List, Union

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .decorators import login_required_message_and_redirect
from .forms import NewListingForm, NewBidForm, NewCommentForm
from .models import User, AuctionListing, Bid, WatchList, Comment


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


def my_listings_view(request):
    listings = AuctionListing.objects.filter(user=request.user)
    return render(request, "auctions/my_listings.html", context=get_listings_context(request, listings=listings))


def watch_list_view(request):
    watch_list = WatchList.objects.filter(user=request.user)

    if watch_list.first():
        listings = [wish.listing for wish in watch_list]
        return render(request, "auctions/watchlist.html", context=get_listings_context(request, listings=listings))
    messages.add_message(request, messages.INFO, "There are no items in your watchlist yet")
    return render(request, "auctions/watchlist.html")


def my_biddings_view(request):
    bidding_list = Bid.objects.filter(user=request.user)
    if bidding_list.first():
        listings = list({bidding.listing for bidding in bidding_list})
        return render(request, "auctions/biddings.html", context=get_listings_context(request, listings=listings))


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
    listing = AuctionListing.objects.get(id=listing_id)
    comments = Comment.objects.filter(listing=listing)
    context = {
        "listing": listing,
        "form": NewBidForm(),
        "comments": comments
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


def change_listing_acitivty_view(request, listing_id: int):
    """
    Open/close the auction of a listing
    """
    listing = AuctionListing.objects.get(id=listing_id)
    listing.active = not listing.active
    listing.save()
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)


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


def categories_view(request):
    categories_unique = AuctionListing.objects.filter(active=True).values_list("category").distinct()
    categories_unique = [c[0] for c in categories_unique if
                         c != AuctionListing._meta.get_field('category').get_default()]

    categories_unique = {
        c: len(AuctionListing.objects.filter(active=True, category=c)) for c in categories_unique
    }

    context = {
        "categories": categories_unique
    }

    return render(request, "auctions/categories.html", context=context)


def category_view(request, category: str):
    listings = AuctionListing.objects.filter(category=category, active=True)
    context = get_listings_context(request, listings=listings)
    context.update({"category": category})
    return render(request, "auctions/category.html", context=context)


def create_comment(request, listing_id: int):
    listing = AuctionListing.objects.get(id=listing_id)
    if request.method == "POST":

        form = NewCommentForm(request.POST)
        if form.is_valid():

            if request.POST.get("Save"):

                comment_value = form.cleaned_data["comment"]

                # Create new entry in the comment table
                comment = Comment(
                    comment=comment_value,
                    user=request.user,
                    listing=listing
                )
                comment.save()
                return redirect("auctions:listing", listing_id)
            elif request.POST.get("Overwrite"):
                comment = Comment.objects.get(id=request.POST.get("comment_id"))
                comment.comment = form.cleaned_data["comment"]
                comment.save()
                return redirect("auctions:listing", listing_id=listing.id)

    context = {
        "listing_id": listing_id,
        "form": NewCommentForm()
    }
    return render(request, "auctions/comment.html", context=context)


def edit_comment(request, listing_id: int, comment_id: str):
    comment = Comment.objects.get(id=comment_id)

    form = NewCommentForm(
        initial={
            "comment": comment.comment
        }
    )

    context = {
        "form": form,
        "listing_id": listing_id,
        "comment_id": comment_id
    }
    return render(request, "auctions/comment.html", context)


def delete_comment(request, listing_id: str, comment_id: str):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect("auctions:listing", listing_id=listing_id)
