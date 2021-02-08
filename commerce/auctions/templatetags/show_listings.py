"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 08/02/2021
"""
from django import template

register = template.Library()


@register.inclusion_tag('auctions/show_listings.html')
def show_listings(listings):
    return {"listings": listings}


def main():
    pass


if __name__ == "__main__":
    main()
