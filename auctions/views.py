from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from .models import Listing, User, Bid, Category, Comment, WatchList




class New_Listing(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('title', 'description', 'starting_price', 'category', 'photo')
        labels = {'title':'', 'description':'', 'starting_price':'', 'category':'', 'photo':''}
        placeholder = {'title'}
        widgets = {'category' : forms.Select(choices=Category.objects.all(), attrs={'class' : 'form-control'}),
                   'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Title'}),
                   'description' :forms.Textarea(attrs={'class' : 'form-control', 'placeholder':'Description'}),
                   'starting_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Starting Price'}),
                   'photo': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Photo'})
                   } 

class New_Bid(forms.ModelForm):
    class Meta:
        model = Bid
        labels = {'bid_amount':''}
        fields = ('bid_amount',)
        widgets = {'bid_amount': forms.NumberInput(attrs={'placeholder':'Make Your Bid'})}


class New_Comment(forms.ModelForm):
    class Meta:
        model = Comment
        labels = {'comment':''}
        fields = ('comment',)
        widgets = {'comment': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Add your Comment'})}

class Add_Watchlist(forms.ModelForm):
    class Meta:
        model = WatchList
        fields = '__all__'

def get_watchlist_count(request):
    user = request.user
    if user.id is None:
        return None
    else:
        watchlist_count = WatchList.objects.filter(watchlist_owner = user).count()
        return watchlist_count

def index(request):
    listings = Listing.objects.all().order_by('id').reverse()
    context = {
        'listings': listings,
        'watchlist_count':get_watchlist_count(request),
        }
    return render(request, "auctions/index.html", context)


def watchlist(request):
    user = request.user
    if user.id is not None:
        if request.method == 'GET':

            context = {
                'watchlist': WatchList.objects.filter(watchlist_owner=user).order_by('added_watchlist_on').reverse(),
                'watchlist_count':get_watchlist_count(request)
                }
            return render(request, 'auctions/watchlist.html', context)
    else:
        return redirect('login')





#LISTING PAGE
def listing(request, listing):
        user = request.user
        item = Listing.objects.get(id=listing)
        comments = Comment.objects.filter(listing_id=listing).order_by('published_on').reverse()
        
        if user.id is not None:
            watchlist_exists = WatchList.objects.filter(watchlist_owner=user, listing_id=item)
            is_in_watchlist = len(watchlist_exists)
        else:
            is_in_watchlist = None

        if request.method == 'GET':
            context = {
                'listing': item,
                'comments': comments,
                'new_bid': New_Bid(),
                'new_comment': New_Comment(),
                'watchlist_count': get_watchlist_count(request),
                'is_in_watchlist': is_in_watchlist
            }
            return render(request, 'auctions/listing_view.html', context)

        if request.method == 'POST':
            bidForm = New_Bid(request.POST)
            commentForm = New_Comment(request.POST)

            #ADDING BID
            if bidForm.is_valid():
                current_bid = bidForm.cleaned_data["bid_amount"]

                #Last bid may return none, for new listings, if makes sure it'd det to 0 for validation
                last_bid = Listing.objects.filter(id=listing).values('latest_bid')
                last_bid = last_bid[0]['latest_bid']
                if last_bid is None:
                    last_bid = 0
                else:
                    last_bid = last_bid

                #starting_price of listing is never 0
                starting_price = Listing.objects.filter(id=listing).values('starting_price')
                starting_price = starting_price[0]['starting_price']

                sold = Listing.objects.filter(id=listing).values('sold')
                sold = sold[0]['sold']

                if (last_bid == 0 and current_bid > starting_price) or (current_bid > last_bid and current_bid > starting_price) and sold == False:
                    highest_bid = Bid.objects.create(
                        bid_amount=current_bid,
                        bid_owner =user,
                        listing_id=item
                        )
                    Listing.objects.filter(id=listing).update(latest_bid=highest_bid)

                    return render(request, 'auctions/success.html', {
                                'message': f"Your bid of {current_bid} has been placed successfully!", 'watchlist_count': get_watchlist_count(request)
                            })

                else:
                    return render(request, 'auctions/success.html', {
                                'message': f"Your bid of {current_bid} is lower than the highest bit or starting price of this item! Please, try again.", 'watchlist_count': get_watchlist_count(request)
                            })
            #ADDING COMMENT
            if commentForm.is_valid():
                comment = commentForm.cleaned_data['comment']
                Comment.objects.create(
                        comment = comment,
                        comment_owner = user,
                        listing_id = item
                        )
                return render(request, 'auctions/success.html', {
                                'message': f"Your comment has been posted to item: {item.title}.", 'watchlist_count': get_watchlist_count(request)
                            })

            #ADD ITEM TO WATCHLIST
            """
            else:
                if len(watchlist_exists) > 0:
        
                    return render(request, 'auctions/success.html', {
                        'message': f" {item.title} is already on your watchlist.", 'watchlist_count': get_watchlist_count(request)
                        })

                WatchList.objects.create(
                        watchlist_owner = user,
                        listing_id = item
                        
                        )

                
                return render(request, 'auctions/success.html', {
                        'message': f" {item.title} has been added to your watchlist.", 'watchlist_count': get_watchlist_count(request)
                        })
            """
            


# List of categories
def categories(request):
    if request.method == 'GET':
        context = {
            'categories': Category.objects.all().order_by('name'),
            'watchlist_count': get_watchlist_count(request)
        }
        return render(request, 'auctions/categories.html', context)

# Lists Item by Category
def category_view(request, category):
    if request.method == 'GET':
        category_name = Category.objects.get(name=category)
                        
        context = {
            'listings': Listing.objects.filter(category=category_name).order_by('id').reverse(),
            'category': category_name,
            'watchlist_count':get_watchlist_count(request)
            }

        return render(request, 'auctions/index.html', context)


#CREATE NEW LISTING
def new_listing(request):
    user = request.user
    if user.id != None:
        if request.method =='POST':
            form = New_Listing(request.POST)

            if form.is_valid():
                title = form.cleaned_data["title"]
                description = form.cleaned_data["description"]
                starting_price = form.cleaned_data["starting_price"]
                photo= form.cleaned_data["photo"]
                category = form.cleaned_data["category"]

                Listing.objects.create(
                    title=title,
                    description=description,
                    starting_price=starting_price,
                    photo=photo,
                    category=category,
                    user_owner_id=request.user
                    )

                return redirect("index")
        else:
            return render (request, "auctions/new_listing.html", {"post": New_Listing(), 'watchlist_count':get_watchlist_count(request)})

    else:
        return redirect('login')

##### USER MANAGEMENT OF LISING #####
##### Mark as sold, delete listing, remove from watchlist
def sold_listing(request, listing):
    if request.method == 'GET':
        listing_item = Listing.objects.get(id=listing)
        listing_item.sold = True
        listing_item.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def delete_listing(request, listing):
    if request.method == 'GET':
        listing = Listing.objects.get(id=listing)
        if listing.user_owner_id == request.user:
            listing.delete()
            return redirect('index')

def remove_from_watchlist(request, listing):
    user = request.user
    item = Listing.objects.get(id=listing)
    if request.method == 'GET':
        watchlist_item = WatchList.objects.get(listing_id=item, watchlist_owner=user.id)
        if watchlist_item.watchlist_owner == request.user:
            watchlist_item.delete()
            return redirect('watchlist')

def add_watchlist(request, listing):
        user = request.user
        item = Listing.objects.get(id=listing)
        watchlist_exists = WatchList.objects.filter(listing_id=item, watchlist_owner=user.id)

        if len(watchlist_exists) > 0:
            return render(request, 'auctions/success.html', {
                'message': f" {item.title} is already on your watchlist.", 'watchlist_count': get_watchlist_count(request)
            })

        WatchList.objects.create(
            watchlist_owner = user,
            listing_id = item
            )
  
        return redirect('watchlist')




##### USER MANAGEMENT OF LISTING #####


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")