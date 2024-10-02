from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", blank=True, related_name="watchers")


class Listing(models.Model):
    def get_admin_url(self):
        return reverse('admin:auctions_listing_change', args=[self.id])
    CATEGORIES = ["Watches", "Other", "Paintings", "Antiques", "Jewelry"]
    def get_category(categories=CATEGORIES):
        return {i: i for i in categories}
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="own_listings")
    item = models.CharField(max_length=40)
    description = models.TextField(max_length=2000)
    photo = models.ImageField(blank=True)
    category = models.CharField(max_length=20, blank=True, choices=get_category, default='Other')
    active_flag = models.BooleanField(default=False)
    post_date = models.DateField(auto_now_add=True)
    post_time = models.TimeField(auto_now_add=True)
    def __str__(self):
        if self.active_flag is True:
            status = "active"
        else:
            status = "not active"
        return f'{self.category} --> {self.item} -> {status}'


class Bid(models.Model):
    def get_admin_url(self):
        return reverse('admin:auctions_bid_change', args=[self.id])
    CURRENCIES = ["EUR", "USD", "RON"]
    def get_currencies(currencies=CURRENCIES):
        return {i: i for i in currencies}
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="own_bids")
    start_bid = models.IntegerField(validators=[MinValueValidator(10)], default=10)
    current_bid = models.IntegerField(null=True, blank=True)
    currency = models.CharField(max_length=3, choices=get_currencies, default='RON')
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, related_name="bid", null=True)
    def __str__(self):
        show =  f'{self.listing.item} ---start---> {self.start_bid} {self.currency}'
        if self.listing.active_flag is True:
            show +=  f' ---current---> {self.current_bid} {self.currency}'
        else:
            pass
        return show


class Comment(models.Model):
    def get_admin_url(self):
        return reverse('admin:auctions_comment_change', args=[self.id])
    comment = models.TextField(max_length=1000)
    post_date = models.DateField(auto_now=True)
    post_time = models.TimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", null=True)
    def __str__(self):
        return f'{self.author} -> {self.listing.item}'

