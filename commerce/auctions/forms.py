"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 04/02/2021
"""

from django.forms import Form, CharField, Textarea, DecimalField, URLField, BooleanField


class NewListingForm(Form):
    title = CharField(label="title", initial="")
    description = CharField(widget=Textarea, label="description", initial="")
    starting_bid = DecimalField(label="starting_bid", initial=0.0, decimal_places=1)
    category = CharField(label="category", initial="", required=False)
    image_url = URLField(label="image_url", initial="", required=False)
    active = BooleanField(label="active", required=True, initial=True)


def main():
    pass


if __name__ == "__main__":
    main()
