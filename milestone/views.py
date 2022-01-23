from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import random
from django.db.models import Q
from django.db.models import CharField, IntegerField, Value, F
from django.db.models import Count
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

#####INDEX####
def matches(request, eventId):


    matches = Like.objects.filter(event=eventId, like=True).values('event_id','event__name', 'food', 'food__name', 'food__ratings', "food__distance", "food__image_url").annotate(like_count=Count('food')).order_by('-like_count', '-food__ratings', 'food__distance')
    events = Event.objects.get(id=eventId)
    
    if not matches:
        matches = None
    else:
        for match in matches:
            if match['like_count'] > 1:
                break
            else:
                matches = None

    print(matches)

    #json_data_2 = json_data.replace('\'', '') #used this as an atempt to replace backslashes.
    #test = Food.objects.annotate(Count('like__event'))
    #return JsonResponse(json_data_2, safe=False) #This retruned backslashes in responese
    #return HttpResponse(json_data) #This did not return backslashes
    return render(request, "milestone/matches.html", {
        "matches": matches,
        "event": events.serialize()
    })


def myevents(request):
    if request.user.is_authenticated:
        myevents=Event.objects.filter(organizer=request.user).order_by("date")
    
        return render(request, "milestone/index.html", {
        "events": [event.serialize() for event in myevents],
        })

    else:
        return render(request, "milestone/login.html")



def count_likes(request, eventId):
    user_events = Event.objects.filter(participants=request.user).order_by("date")

    return JsonResponse([event.serialize() for event in user_events], safe=False)


def index(request):
    if request.user.is_authenticated:
        user_events = Event.objects.filter(participants=request.user).order_by("date")

        return render(request, "milestone/index.html", {
            "events": [event.serialize() for event in user_events],
        })

    else:
        return render(request, "milestone/login.html")

@csrf_exempt
@login_required
def delete_event(request, eventId):
    if request.method == "POST":
        try:
            Event.objects.filter(id=eventId).delete()
            Like.objects.filter(id=eventId).delete()
            return JsonResponse({
                    "message": "event has been deleted"
                }, status=200)
        except:
            return JsonResponse({
                    "error": "not able to delete"
                }, status=400)


@csrf_exempt
@login_required
def like(request, eventId):
    if request.method == "POST":
        data = json.loads(request.body)
        foodId = data.get("foodId", "")
        liked = data.get("like", "")
        event = Event.objects.get(id=eventId)
        food = Food.objects.get(id=foodId)
        try:
            user_event_likes = Like.objects.get(event=event, user=request.user.id, food=food)
            print(user_event_likes.like)
            print(liked)
            if user_event_likes.like != liked:
                user_event_likes.like = liked
                user_event_likes.save()
            else:
                pass
        except:
            user_event_likes = Like(event=event, user=request.user, food=food, like=liked)
            user_event_likes.save()
        return eventview(request, eventId)


   

def foods(delivery, pickup, dinein, user , eventId):
    foods = Food.objects.filter(Q(delivery=delivery) | Q(pickup=pickup) | Q(dinein=dinein)).order_by('?')
    for item in foods:
        try:
            Like.objects.get(user=user, food=item, event=eventId)

        except Like.DoesNotExist:
            food = Food.objects.get(id=item.id)
            break
    
    try:
        return food

    except:
        food = Food.objects.filter(Q(delivery=delivery) | Q(pickup=pickup) | Q(dinein=dinein)).order_by('?').first()
        return food


def eventview(request, eventId):
    if request.user.is_authenticated:
        if request.method == "GET":
            event = Event.objects.get(id=eventId)
            food_prompt = foods(event.delivery, event.pickup, event.dinein, request.user , eventId)
            try:
                like_status = Like.objects.get(user=request.user, event=eventId, food=food_prompt)
                liked = like_status.like
            except Like.DoesNotExist:
                liked = None

            likes = Like.objects.filter(event=eventId, food=food_prompt, like=True).exclude(user=request.user).count()
            if liked == False:
                liked = "You did not like this before"
            elif liked == True:
                liked = "You liked this before"
            else:
                liked = "You haven't given your opinion"

            return render(request, "milestone/event.html", { 
                "event": event.serialize(),
                "food": food_prompt,
                "liked": liked,
                "likes": likes
            })


        
    
    else:
        return render(request, "milestone/login.html")



@csrf_exempt
@login_required
def event(request):
    if request.method == "POST":
        data = json.loads(request.body)
        eventId = data.get("eventId")

        if eventId != None:
            event_name = data.get("event_name", "")
            delivery= data.get("delivery", "")
            pickup= data.get("pickup", "")
            dinein= data.get("dinein", "")
            date= data.get("date", "")

            event = Event.objects.get(id=eventId)
            event.name = event_name
            event.delivery = delivery
            event.pickup = pickup
            event.dinein = dinein
            event.date = date
            event.save()

            return HttpResponseRedirect(reverse("index")) 

        else:
            emails = [email.strip() for email in data.get("participants").split(",")]
            if emails == [""]:
                return JsonResponse({
                    "error": "At least one recipient required."
                }, status=400)

            event_name = data.get("event_name", "")
            delivery= data.get("delivery", "")
            pickup= data.get("pickup", "")
            dinein= data.get("dinein", "")
            date= data.get("date", "")


            participants = []
            for email in emails:
                try:
                    user = User.objects.get(email=email)
                    participants.append(user.id)

                except User.DoesNotExist:
                    return JsonResponse({
                        "error": f"User with email {email} does not exist."
                    }, status=400)
        
            event = Event(
                name=event_name,
                organizer=request.user,
                delivery=delivery,
                pickup=pickup,
                dinein=dinein,
                date=date
            )
            event.save()
            for participant in participants:
                event.participants.add(participant)
            organizer = User.objects.get(email=request.user.email) #adds organizer as participant
            event.participants.add(organizer) #adds organizer as participant
            event.save()


            return HttpResponseRedirect(reverse("index")) 
    else:
        return HttpResponseRedirect(reverse("index"))



def events(request):
    if request.user.is_authenticated:
        user_events = Event.objects.filter(participants=request.user)

    return JsonResponse([event.serialize() for event in user_events], safe=False)





























#LOGIN VIEWS
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
            return render(request, "milestone/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "milestone/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname= request.POST["firstname"]
        lastname= request.POST["lastname"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "milestone/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, first_name=firstname, last_name=lastname)
            user.save()
        except IntegrityError:
            return render(request, "milestone/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "milestone/register.html")
