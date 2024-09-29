from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from auctions.models import User, Listing, Bid, Commment

# Register your models here.

class Admin(UserAdmin):
    admin.site.register(User, UserAdmin)
    admin.site.register(Listing)
    admin.site.register(Bid)
    admin.site.register(Commment)