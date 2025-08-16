from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu_view, name='menu'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='meal_web/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('my-subscription/', views.my_subscription, name='my_subscription'),
    path('toggle-paid/', views.toggle_paid, name='toggle_paid'),
    path('toggle-pause/', views.toggle_pause, name='toggle_pause'),
    path('change-diet/', views.change_diet, name='change_diet'),
]
