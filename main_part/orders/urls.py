from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payment', views.payment, name='payment'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('cod_ordercomplete/', views.cod_ordercomplete, name='cod_ordercomplete'),

    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
]
