from django.contrib.auth.models import AbstractUser
import uuid
from django.db import models
from django.utils import timezone
from datetime import datetime


class User(AbstractUser):
    pass

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Listing(models.Model):

    #Listing Details
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1280, blank=True)
    comments = models.ManyToManyField('Comment', related_name='comments_in_the_auction', blank=True)
    photo = models.CharField(max_length=1280, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='listing_category', default=3)
    user_owner_id = models.ForeignKey('User',on_delete=models.CASCADE, related_name='listing_owner')
    published_on = models.DateTimeField(default=timezone.now)

    #Bid Attributes
    starting_price = models.FloatField()
    bids = models.ManyToManyField('Bid', related_name='listing_bids', blank=True)
    latest_bid = models.ForeignKey('Bid', on_delete=models.CASCADE, related_name='last_listingbid', blank=True, null=True)
    sold = models.BooleanField(default=False)


    def published_date(self):
        return self.date.strftime('%m/%d/%Y')

    def _str_(self):
        return self.title

class Bid(models.Model):
    bid_amount = models.FloatField()
    bid_owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    listing_id = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE
    )
    bid_time = models.DateTimeField(default=timezone.now)

    def published_date(self):
        return self.date.strftime('%m/%d/%Y')
    
    def _str_(self):
        return self.bid_amount
        



class Comment(models.Model):
    comment = models.TextField(max_length=128)
    comment_owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    listing_id = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE
    )
    published_on = models.DateTimeField(default=timezone.now)

    def published_date(self):
        return self.date.strftime('%m/%d/%Y')
    
    def _str_(self):
        return self.comment



class WatchList(models.Model):
    id = models.AutoField(primary_key=True)

    watchlist_owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='watchlist_owner',
        default=1
    )

    listing_id = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        default=16
    )

    added_watchlist_on = models.DateTimeField(default=timezone.now)

    def published_date(self):
        return self.date.strftime('%m/%d/%Y')
    
    def _str_(self):
        return self.id
