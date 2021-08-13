from django.contrib import admin

# Register your models here.

from .models import User, Listing, Comment, Bid, Category, WatchList

# Register your models here.

admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(WatchList)
