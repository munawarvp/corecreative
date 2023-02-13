from django.urls import path
from . import views
urlpatterns = [
    path('', views.store, name='store'),
    path('accessories/', views.accessories, name='accessories'),
    path('category/', views.category, name='category'),
    path('category/<slug:category_slug>/', views.store, name='product_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),

    

    path('search/', views.search, name='search'),

    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review')
]