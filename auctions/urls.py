from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

app_name = "auction"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:listing>/listing", views.listing_view, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<str:listing>/comment", views.add_comment, name="add_comment"),
    path("add", views.add_listing, name="add_listing"),
    path("<str:listing>/raise", views.bid_raise, name="bid_raise"),
    path("watchlist", views.watchlist_view, name="watchlist")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
