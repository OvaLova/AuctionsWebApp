from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    CATEGORIES = ["Watches", "Other", "Paintings", "Antiques", "Jewelry"]
    def get_category(categories=CATEGORIES):
        return {i: i for i in categories}
    item = models.CharField(max_length=40)
    description = models.TextField(max_length=2000)
    photo = models.ImageField(blank=True)
    category = models.CharField(max_length=20, blank=True, choices=get_category, default='Other')
    active_flag = models.BooleanField(default=False)
    def __str__(self):
        if self.active_flag is True:
            status = "active"
        else:
            status = "not active"
        return f'{self.category} --> {self.item} -> {status}'

class Bid(models.Model):
    CURRENCIES = ["EUR", "USD", "RON"]
    def get_currencies(currencies=CURRENCIES):
        return {i: i for i in currencies}
    start_bid = models.IntegerField(validators=[MinValueValidator(10)], default=10)
    current_bid = models.IntegerField(null=True, blank=True)
    currency = models.CharField(max_length=3, choices=get_currencies, default='RON')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid", null=True)
    def __str__(self):
        show =  f'{self.listing.item} ---start---> {self.start_bid} {self.currency}'
        if self.listing.active_flag is True:
            show +=  f' ---current---> {self.current_bid} {self.currency}'
        else:
            pass
        return show


class Commment(models.Model):
    comment = models.CharField(max_length=1000)
    post_date = models.DateField( auto_now=True)
    post_time = models.TimeField( auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", null=True)
    def __str__(self):
        return f'{self.author} -> {self.listing.item}'

