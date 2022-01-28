from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("events", views.events, name="events"),
    path("event", views.event, name="event"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('event/<int:eventId>', views.eventview, name='eventview'),
    path('like/<int:eventId>', views.like, name='eventview'),
    path('myevents', views.myevents, name='myevents'),
    path('delete/<int:eventId>', views.delete_event, name='delete_event'),
    path('count_likes/<int:eventId>', views.count_likes, name='count_likes'),
    path('matches/<int:eventId>', views.matches, name='matches'),
    path('api-auth/', include('rest_framework.urls'))

]
