from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from auctions.models import User, Listing, Bid, Comment
from django.utils.html import format_html_join


# Register your models here.

class CustomUserAdmin(UserAdmin):
    readonly_fields = UserAdmin.readonly_fields + ("own_listings", "own_comments", "own_bids")
    fieldsets = UserAdmin.fieldsets + (
            ('Additional Info', {'fields': ('watchlist','own_listings','own_comments','own_bids')}),
    )
    def own_listings(self, obj):
        listings = Listing.objects.filter(owner=obj)
        return format_html_join(
            '\n',
            '<a href="{}">{}</a><br>',
            ((listing.get_admin_url(), listing) for listing in listings)
        )
    def own_comments(self, obj):
        comments = Comment.objects.filter(author=obj)
        return format_html_join(
            '\n',
            '<a href="{}">{}</a><br>',
            ((comment.get_admin_url(), comment) for comment in comments)
        )
    def own_bids(self, obj):
        bids = Bid.objects.filter(owner=obj)
        return format_html_join(
            '\n',
            '<a href="{}">{}</a><br>',
            ((bid.get_admin_url(), bid) for bid in bids)
        )
    filter_horizontal = ('watchlist',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)