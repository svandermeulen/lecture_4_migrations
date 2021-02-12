"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 04/02/2021
"""

from django.forms import Form, CharField, Textarea, DecimalField, URLField, BooleanField, DateTimeField, ModelForm, \
    TextInput

from .models import Bid


class NewListingForm(Form):
    title = CharField(label="title", initial="")
    description = CharField(widget=Textarea, label="description", initial="")
    starting_bid = DecimalField(label="starting_bid", initial=0.0, decimal_places=2)
    category = CharField(label="category", initial="", required=False, empty_value="No category listed")
    image_url = URLField(label="image_url", initial="", required=False)


class NewBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ('bid',)
        widgets = {
            'bid': TextInput(attrs={'placeholder': 0.00})
        }


def main():
    pass


if __name__ == "__main__":
    main()
