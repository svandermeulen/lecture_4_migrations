from django.urls import path, register_converter

from . import views, converters

register_converter(converters.IdToListingTitle, "listingconv")


app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("bid/listing/<listingconv:listing_id>", views.place_bid, name="bid"),
    path("create", views.create_listing_view, name="create"),
    path("watchlist", views.watch_list_view, name="watchlist"),
    path("add-to-watchlist/listing/<listingconv:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove-from-watchlist/listing/<listingconv:listing_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("mylistings", views.my_listings_view, name="my_listings"),
    path("mybiddings", views.my_biddings_view, name="my_biddings"),
    path("listing/<listingconv:listing_id>", views.listing_view, name="listing"),
    path("edit/listing/<listingconv:listing_id>", views.edit_listing_view, name="edit"),
    path("close/listing/<listingconv:listing_id>", views.change_listing_activty_view, name="open_close"),
    path("categories", views.categories_view, name="categories"),
    path("category/<category>", views.category_view, name="category"),
    path("comment/listing/<listingconv:listing_id>", views.comment.create_comment, name="comment"),
    path("comment/edit/<str:comment_id>/listing/<listingconv:listing_id>", views.edit_comment, name="edit_comment"),
    path("comment/delete/<str:comment_id>/listing/<listingconv:listing_id>", views.delete_comment, name="delete_comment")
]
