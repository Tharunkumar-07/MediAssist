# urls.py in your Django app
from django.contrib import admin
from django.urls import path
from .views import chatbot, HomePage,SignupPage,LoginPage,LogoutPage

urlpatterns = [
    path('',HomePage,name='home'),
    path('signup/',SignupPage,name='signup'),
    path('login/',LoginPage,name='login'),
    path('logout/',LogoutPage,name='logout'),
    # path('', welcome_message, name='welcome'),
    path('chatbot/', chatbot, name='chatbot'),
    # Add other URL patterns for your app here
]
