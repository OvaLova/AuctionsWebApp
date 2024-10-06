from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

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
            next_url = request.POST.get("next", "/")
            return redirect(next_url)
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
    try:
        if listing in Listing.objects.filter(watchers=request.user):
            watch_flag = True
        else:
            watch_flag = False
    except TypeError:
        watch_flag = None
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments,
        "watch_flag": watch_flag
    })


@login_required
def add_comment(request, listing):
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


@login_required
def add_listing(request):
    if request.method == "GET":
        categories = Listing.CATEGORIES
        currencies = Bid.CURRENCIES
        return render(request, "auctions/add.html", {
            "categories": categories,
            "currencies": currencies
        })
    else:
        new = Listing.objects.create(owner=request.user, item=request.POST.get("item"), category=request.POST.get("category"), description=request.POST.get("description"), photo=request.FILES.get("photo"))
        activate = request.POST.get("activate")
        bid = new.bid
        bid.start_bid = int(request.POST.get("bid"))
        bid.currency = request.POST.get("currency")
        if activate == "on":
            new.active_flag = True
        else:
            new.active_flag = False
        bid.save()
        new.save()
        return HttpResponseRedirect(reverse("auction:listing", kwargs={"listing": request.POST.get("item")}))


@login_required
def bid_raise(request, listing):
    listing = Listing.objects.get(item=listing)
    bid = Bid.objects.get(listing=listing)
    new_bid = request.POST.get("new_bid")
    if new_bid is None:
        return HttpResponseRedirect(reverse("auction:listing", kwargs={"listing": listing.item}))
    else:
        pass
    if bid.current_bid is None:
        old_bid = bid.start_bid
    else:
        old_bid = bid.current_bid
    if int(new_bid) - old_bid >= 1 and int(new_bid) > bid.start_bid:
        bid.current_bid = new_bid
        bid.owner = request.user
        bid.save()
        return HttpResponseRedirect(reverse("auction:listing", kwargs={"listing": listing.item}))
    else:
        comments = list(Comment.objects.filter(listing=listing))
        if listing in Listing.objects.filter(watchers=request.user):
            watch_flag = True
        else:
            watch_flag = False
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": comments,
            "watch_flag": watch_flag,
            "warning": "Enter a bid larger than the last one!"
        })


@login_required
def watchlist_view(request):
    requester = request.user
    listings = Listing.objects.filter(active_flag=True)
    watchlist = []
    if request.method == "GET":
        for listing in listings:
            if requester in listing.watchers.all():
                watchlist.append(listing)
            else:
                pass
        return render(request, "auctions/watchlist.html", {
            "listings": watchlist
        })
    else:
        listing_id = request.POST.get("listing_id")
        listing = Listing.objects.get(id=listing_id)
        if listing in Listing.objects.filter(watchers=requester):
            requester.watchlist.remove(listing)
            return HttpResponseRedirect(reverse("auction:listing", kwargs={"listing": listing.item}))
        else:
            requester.watchlist.add(listing)
            return HttpResponseRedirect(reverse("auction:listing", kwargs={"listing": listing.item}))


@login_required
def close(request, listing):
    listing = Listing.objects.get(item=listing)
    if request.user == listing.owner:
        listing.closed_flag = True
        listing.save()
    else:
        pass
    return HttpResponseRedirect(reverse("auction:listing", kwargs={"listing": listing.item}))


@login_required
def edit_view(request, listing):
    listing = Listing.objects.get(item=listing)
    if request.method == "GET":
        if listing.bid.current_bid == None:
            bid = listing.bid.start_bid
        else:
            bid = listing.bid.current_bid
        if request.user == listing.owner:
            return render(request, "auctions/edit.html", {
                "categories": Listing.CATEGORIES,
                "currencies": Bid.CURRENCIES,
                "listing": listing,
                "bid": bid,
            })
        else:
            return HttpResponseRedirect(reverse("auction:listing", kwargs={"listing": listing.item}))
    elif request.method == "POST":
        listing.item = request.POST.get("item")
        listing.category = request.POST.get("category")
        listing.description = request.POST.get("description")
        if request.FILES.get("photo"):
            listing.photo = request.FILES.get("photo")
        bid = listing.bid
        bid.start_bid = request.POST.get("bid")
        bid.currency = request.POST.get("currency")
        if request.POST.get("activate") == "on":
            listing.active_flag = True
        else:
            listing.active_flag = False
        bid.save()
        listing.save()
        return HttpResponseRedirect(reverse("auction:listing", kwargs={"listing": request.POST.get("item")}))


def categories(request):
    categories = Listing.CATEGORIES
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category(request, category):
    listings = Listing.objects.filter(active_flag=True, category=category)
    return render(request, "auctions/category.html", {
        "listings": listings,
        "category": category
    })


@login_required
def own_listings(request):
    listings = Listing.objects.filter(owner=request.user)
    return render(request, "auctions/own.html", {
        "listings": listings,
    })