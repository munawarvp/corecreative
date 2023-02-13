from django.contrib import admin
from .models import Wishlist,Wishlist_item

# Register your models here.

admin.site.register(Wishlist)
admin.site.register(Wishlist_item)