"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 15/02/2021
"""
from django.shortcuts import render

from ..models import AuctionListing
from ..views.index import get_listings_context


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


def main():
    pass


if __name__ == "__main__":
    main()
