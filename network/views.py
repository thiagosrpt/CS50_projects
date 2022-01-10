import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from django.db.models.fields.related import ManyToManyField
from django.core import serializers
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder


from .models import User, Post

# ------------- INDEX -----------------

def index(request):
    allPosts = Post.objects.all().order_by("-date")

    if request.user.is_authenticated:
        likedPosts = request.user.userLikes.all()
    else:
        likedPosts = []


    #required for paginaton decorators
    paginator = Paginator(allPosts, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_page)

    #required controls pagination numbers
    page_list = []
    i = 0
    for page in paginator:
        i = 1 + i
        page_list.append(i)
    print(page_list)


    return render(request, "network/index.html", {
        "posts": posts,
        "liked_posts": likedPosts,
        "username": request.user,
        "follows": False,
        "page_list": page_list #requires for paginaton numbers at the bottom of page
    })

def following(request):

    if request.user.is_authenticated:
        user = request.user
        #if user.id is not None:
            #if request.method == 'GET':
        posts =[]
        for user in request.user.following.all():
            following_posts = Post.objects.filter(creator = user).order_by("-date")
            for post in following_posts:
                posts.append(post)
                posts = sorted(posts, key=lambda k: k.id, reverse= True)

        print(posts)
        following =[]
        username = User.objects.get(username = request.user.username)
        for user in username.following.all():
            following.append(user.username)

        if request.user.is_authenticated:
            likedPosts = request.user.userLikes.all()
        else:
            likedPosts = []
        
        #required for paginaton decorators
        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_page)

        #required controls pagination numbers
        page_list = []
        i = 0
        for page in paginator:
            i = 1 + i
            page_list.append(i)
        print(page_list)


        return render(request, 'network/index.html', {
            "posts": posts,
            "liked_posts": likedPosts,
            "username": username.pk,
            "user_id": request.user.id,
            "following": following,
            "page_list": page_list #requires for paginaton numbers at the bottom of page
        })
    
    else:
        return HttpResponseRedirect(reverse("index")) 

#infinitive scroll???
def posts(request):
        
    allPosts = serializers.serialize('json', Post.objects.all().order_by("-date"))
    #p = Paginator(allPosts, 3)
    #counter = p.count #Number of items across all pages
    #numberOfPages = p.num_pages

    #json_str = json.dumps()
    #test_data = json_str

    #page = request.GET.get('postId')
    start = int(request.GET.get("start") or 1)
    end = int(request.GET.get("end") or (start))

    data = serializers.serialize('json', Post.objects.all().order_by("-date")[start-1:end])

    #data_test = allPosts

    # Working before >>> return JsonResponse({ "posts": allPosts })

    #return JsonResponse(allPosts, content_type="text/json-comment-filtered", safe=False)

    return HttpResponse(data.serialize('json'))

def load(request):
    allPosts = Post.objects.all().order_by("-date")
    start = int(request.GET.get("start") or 1)
    end = int(request.GET.get("end") or (start))
    posts =[]

    for p in allPosts:
        posts.append(p.serialize())


    data = Post.objects.all().order_by("-date")[start-1:end]

    #data_test = allPosts

    # Working before >>> return JsonResponse({ "posts": allPosts })

    #return JsonResponse(data, content_type="application/json", safe=False)

    return HttpResponse(p.serialize(), content_type="text/json-comment-filtered")
    

# ------------- END INDEX -----------------
@csrf_exempt
@login_required
def editpost(request, post_id):
    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.body)
        new_content = data.get("new_content", "")
        post = Post.objects.filter(pk = post_id).update(text_content=new_content)
        post = Post.objects.get(pk = post_id)
        post.save()
        print(post)
        return JsonResponse({"message": "message has been posted"}, status=201)

    return JsonResponse({"error": "message failed to post."}, status=400)

@csrf_exempt
@login_required
def follow(request, username):
    data = json.loads(request.body)
    profile_user = data.get("profile_name", "")
    follow_request = data.get("follow_request", "")
    user_following = User.objects.get(id = request.user.id)
    user_follower = User.objects.get(username = username)
    print(profile_user)
    print(follow_request)

    if request.method == "POST":
        if follow_request == "Follow":
            user_following.following.add(user_follower) # adds the target profile to following fields of logged in user.
            user_follower.followers.add(user_following) # adds user logged in as follower of target profile.
            return JsonResponse({"message": "message has been posted"}, status=200)

        elif follow_request == "Unfollow":
            user_following.following.remove(user_follower) # adds the target profile to following fields of logged in user.
            user_follower.followers.remove(user_following) # adds user logged in as follower of target profile.
            return JsonResponse({"message": "message has been posted"}, status=200)

        else:
            return JsonResponse({"error": "request failed."}, status=400)
    else:
        return JsonResponse({"error": "request failed."}, status=400)

#Profile
def profile(request, username):
    user = User.objects.get(username = username) #profile user
    try:
        User.objects.get(id=request.user.id, following=user.id)
        follows = True
    except:
        follows = False
    
    print(follows)

    

    if request.user.is_authenticated:
        liked_posts = request.user.userLikes.all()

    else:
        liked_posts = []

    posts = Post.objects.filter(creator = user.id).order_by('-date')


    #required for paginaton decorators
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_page)

    #required controls pagination numbers
    page_list = []
    i = 0
    for page in paginator:
        i = 1 + i
        page_list.append(i)
    print(page_list)



    followers = user.followers.count()
    following = user.following.count()
    return render(request, 'network/index.html', {
        "posts": posts,
        "liked_posts": liked_posts,
        "username": user, #profile user
        "profile_user": user.username,
        'followers_count': followers,
        'following_count': following,
        "follows": follows, #shows list of usernames logged in user follows.
        "page_list": page_list #requires for paginaton numbers at the bottom of page
        })

#--------------- NEW POSTS ------------

@csrf_exempt
@login_required
def createpost(request):
    if request.method == "POST":
        data = json.loads(request.body)

        post = data.get("post", "")

        print(f'str(request.user)={str(request.user)}')
        post = Post(
            creator = request.user,
            text_content = post
        )
        post.save()
        print(post)
        return JsonResponse({"message": "message has been posted"}, status=201)

    return JsonResponse({"error": "message failed to post."}, status=400)

    

@csrf_exempt
@login_required
def likes(request, post_id):

    data = json.loads(request.body)
    post = Post.objects.get(pk = post_id)
    user = request.user
    
    if request.method == 'POST':

        if data.get('like') == True:
            post.likes.add(user)
            post.save
            return HttpResponse(status=200)

        else:
            post.likes.remove(post.likes.get(pk = user.id))
            post.save()
            return HttpResponse(status=200)
    
    else:
        return HttpResponseRedirect(reverse("index")) 

#--------

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
