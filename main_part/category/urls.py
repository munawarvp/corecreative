from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search')
]
