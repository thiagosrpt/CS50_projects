from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User) #Allow users to be managed via admin
admin.site.register(Post) #Allow posts to be managed via admin
