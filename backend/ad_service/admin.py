from django.contrib import admin

from .models import ADGroup, ADUser

admin.site.register((ADGroup, ADUser))
