from django.urls import path, register_converter

from . import views, converters

register_converter(converters.IdToListingTitle, "idtitle")


app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("bid/<idtitle:listing_id>", views.place_bid, name="bid"),
    path("create", views.create_listing_view, name="create"),
    path("listing/<idtitle:listing_id>", views.listing_view, name="listing"),
    path("edit/<idtitle:listing_id>", views.edit_listing_view, name="edit"),
    path("close/<idtitle:listing_id>", views.close_listing_view, name="close")
]
