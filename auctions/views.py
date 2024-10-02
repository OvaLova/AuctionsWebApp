from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Comment, Bid


def index(request):
    listings = Listing.objects.filter(active_flag=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auction:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auction:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auction:index"))
    else:
        return render(request, "auctions/register.html")
    

def listing_view(request, listing):
    listing = Listing.objects.get(item=listing)
    comments = list(Comment.objects.filter(listing=listing))
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments
    })


def add_comment(request, listing):
    if request.user.is_authenticated:
        listing = Listing.objects.get(item=listing)
        if request.method == "POST":
            comment = request.POST.get("comment")
            author = request.user
            Comment(comment=comment, author=author, listing=listing).save()
            return HttpResponseRedirect(reverse("auction:listing", kwargs={"listing": listing.item}))
        else:
            comments = list(Comment.objects.filter(listing=listing))
            return render(request, "auctions/comment.html", {
                "listing": listing,
                "comments": comments
        })
    else:
        return HttpResponseRedirect(reverse("auction:login"))


def add_listing(request):
    categories = Listing.CATEGORIES
    return render(request, "auctions/add.html", {
        "categories": categories,
    })


def bid_raise(request, listing):
    listing = Listing.objects.get(item=listing)
    bid = Bid.objects.get(listing=listing)
    new_bid = request.POST.get("new_bid")
    bid.current_bid = new_bid
    bid.save()
    return HttpResponseRedirect(reverse("auction:listing", kwargs={"listing": listing.item}))
    

