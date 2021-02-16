"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 15/02/2021
"""
from django.shortcuts import redirect, render

from ..forms import NewCommentForm
from ..models import AuctionListing, Comment


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


def main():
    pass


if __name__ == "__main__":
    main()
