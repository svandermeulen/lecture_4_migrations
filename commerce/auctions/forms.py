"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 04/02/2021
"""

from django.forms import Form, CharField, Textarea, DecimalField, URLField, BooleanField, DateTimeField


class NewListingForm(Form):
    title = CharField(label="title", initial="")
    description = CharField(widget=Textarea, label="description", initial="")
    starting_bid = DecimalField(label="starting_bid", initial=0.0, decimal_places=2)
    category = CharField(label="category", initial="", required=False, empty_value="No Category Listed")
    image_url = URLField(label="image_url", initial="", required=False)


class NewBidForm(Form):
    bid = DecimalField(label="bid", initial=0.0, decimal_places=2)


def main():
    pass


if __name__ == "__main__":
    main()
