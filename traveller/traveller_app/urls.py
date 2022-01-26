from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('register', RegisterUserView.as_view()),
    path('login', LoginUserView.as_view()),
]
