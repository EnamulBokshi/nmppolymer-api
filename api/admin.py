from django.contrib import admin
from .models import Category,Slider, Products, Slider, News
# Register your models here.
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Slider)
admin.site.register(News)
