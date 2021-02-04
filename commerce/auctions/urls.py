from django.urls import path

from . import views

app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("bid/<str:listing_id>", views.place_bid, name="bid"),
    path("create", views.create_listing_view, name="create"),
    path("listing/<str:listing>", views.listing_view, name="listing")
]
