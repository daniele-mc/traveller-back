from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('register', RegisterUserView.as_view()),
    path('login', LoginUserView.as_view()),
    path('user', GetUserView.as_view()),
    path('photo', GetPhotoView.as_view()),
    path('create/travel', CreateTravelView.as_view()),
    path('travel', TravelView.as_view()),
    path('travel/delete/<id>', TravelView.as_view()),
    path('travel/inactive/<id>', TravelInactiveView.as_view()),
    path('travel/active/<id>', TravelActiveView.as_view()),
    path('get_all/travel', GetAllTravelsView.as_view()),
    path('create/route', CreateRouteView.as_view()),
    path('route/<id>', RouteView.as_view()),
    path('create/accommodation', CreateAccommodationView.as_view()),
    path('accommodation/<id>', AccommodationView.as_view()),
    path('create/ticket', CreateTicketView.as_view()),
    path('ticket/<id>', TicketView.as_view()),
    path('create/backpack_item', CreateBackpackItemView.as_view()),
    path('backpack_item/<id>', BackpackItemView.as_view()),
]
