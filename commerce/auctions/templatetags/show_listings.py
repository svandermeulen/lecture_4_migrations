"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 08/02/2021
"""
from typing import List

from django import template
from django.db.models import QuerySet

register = template.Library()


@register.inclusion_tag('auctions/show_listings.html')
def show_listings(request, listings: QuerySet, wished: List[bool]) -> dict:
    return {
        "request": request,
        "listings": listings,
        "wished": wished
    }


def main():
    pass


if __name__ == "__main__":
    main()
