from django.contrib import admin
from .models import Wishlist,Wishlist_item,Wishlists

# Register your models here.

admin.site.register(Wishlist)
admin.site.register(Wishlist_item)
admin.site.register(Wishlists)