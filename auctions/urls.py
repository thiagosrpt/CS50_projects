from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listing/<str:listing>", views.listing, name="listing"),

    path("categories/<str:category>", views.category_view, name="categories"), 
    path("categories", views.categories, name="categories"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("sold_listing/<str:listing>", views.sold_listing, name="sold_listing"),
    path("delete_listing/<str:listing>", views.delete_listing, name="delete_listing"),
    path("remove_from_watchlist/<str:listing>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("add_watchlist/<str:listing>", views.add_watchlist, name="add_watchlist")
]