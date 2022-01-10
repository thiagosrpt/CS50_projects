
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    #Original Urls
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.posts, name="posts"), #posts api brings posts by ranking order from latest to earliers.
    path("load", views.load, name="load"),
    path("following", views.following, name='following'),
    path('likes/<int:post_id>', views.likes, name='likes'),
    path("createpost", views.createpost, name="createpost"),
    path('editpost/<int:post_id>', views.editpost, name='editpost'),
    path("follow/<str:username>", views.follow, name='follow'),
    

    ##MUST BE LAST ACTIVE VIEW##
    path("profile/<str:username>", views.profile, name='profile'),
    path("<str:username>", views.profile, name='profile')
    

    #Added Urls
    #path('newpost', views.newpost, name='newpost'),
    #path('edited_post/<int:post_id>', views.edited_post, name='edited_post'),
    
    #path('is_follow/<str:name>', views.is_follow, name='is_follow'),

    #path('profile/is_follow/<str:name>', views.is_follow, name='is_follow'),
    #path('profile/<str:name>/follow', views.follow, name='follow'),
    #path('profile/edited_post/<int:post_id>', views.edited_post, name='edited_post'),
    #path('profile/count/<str:name>', views.count, name='count'),
    #path('likes/<int:post_id>', views.likes, name='likes'),
    #path('profile/likes/<int:post_id>', views.likes, name='likes')
]