from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token> ', views.activate, name='activate'),
    
    path("my_account/", views.my_account, name='my_account'),
    path("my_orders/", views.my_orders, name='my_orders'),
    path("single_order/<int:order_id>/", views.single_order, name='single_order'),

    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('resetpassword_validate/<uidb64>/<token> ', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),

    path('change_address/', views.change_address, name='change_address'),

    
    # path('unblock/<int:user_id>/', views.unblock, name='unblock'),
]