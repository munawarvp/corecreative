from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_panel, name='admin_panel'),
    path('user_list/', views.user_list, name='user_list'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),

    path('categoy_page/', views.category_page, name='category_page'),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_category/<int:cat_id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:cat_id>/', views.delete_category, name='delete_category'),


    path('product_page/', views.product_page, name='product_page'),
    path('product_view/<int:prod_id>/', views.product_view, name='product_view'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:prod_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:prod_id>/', views.delete_product, name='delete_product'),

    path('order_page/', views.order_page, name='order_page'),
    path('order_view/<int:order_id>/', views.order_view, name='order_view'),
    path('update_order/<int:order_id>/', views.update_order, name='update_order'),

    path('search/', views.search, name='search')
]