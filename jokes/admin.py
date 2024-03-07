from django.contrib import admin
from .models import AppUser, Category, Jokes

admin.site.register(AppUser)
admin.site.register(Jokes)
admin.site.register(Category)