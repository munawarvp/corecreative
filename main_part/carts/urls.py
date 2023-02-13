from django.urls import path
from . import views

urlpatterns = [
    path('', views.carts, name='carts'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),

    path('addtocart/<int:prod_id>/', views.addtocart, name='addtocart'),
    path('removefromcart/<int:prod_id>/', views.removefromcart, name='removefromcart'),
    path('deletecartitem/<int:prod_id>/', views.deletecartitem, name='deletecartitem'),

    path('checkout/', views.checkout, name='checkout')

]