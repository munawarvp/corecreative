"""main_part URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name='home'),
    path("accounts/", include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path("store/", include('store.urls')),
    path("cart/", include('carts.urls')),
    path("admin_panel/", include('admin_panel.urls')),
    path("search/", views.search, name='search'),
    path("page404/", views.page404, name='page404'),
    path("wishlist", include('wishlist.urls')),
    path("orders", include('orders.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "main_part.views.page404"