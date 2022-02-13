from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', ]

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, user, validated_data):
        user.username = validated_data['username']
        user.email = validated_data['email']
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
        user.save()
        return user


class ExtraUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraUser
        fields = ['photo', 'user']


class TravelSerializer(serializers.ModelSerializer):
    routes = serializers.SerializerMethodField()
    accommodations = serializers.SerializerMethodField()
    tickets = serializers.SerializerMethodField()
    backpack_items = serializers.SerializerMethodField()

    class Meta:
        model = Travel
        fields = ['title', 'date_start', 'date_end',
                  'active', 'user', 'id', 'routes', 'accommodations', 'tickets', 'backpack_items']

    def get_routes(self, travel):
        route = Route.objects.filter(travel=travel)
        route_data = RouteSerializer(route, many=True).data
        return route_data

    def get_accommodations(self, travel):
        accommodation = Accommodation.objects.filter(travel=travel)
        accommodation_data = AccommodationSerializer(
            accommodation, many=True).data
        return accommodation_data

    def get_tickets(self, travel):
        ticket = Ticket.objects.filter(travel=travel)
        ticket_data = TicketSerializer(ticket, many=True).data
        return ticket_data

    def get_backpack_items(self, travel):
        backpack_item = BackpackItem.objects.filter(travel=travel)
        backpack_item_data = BackpackItemSerializer(
            backpack_item, many=True).data
        return backpack_item_data


class BackpackItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackpackItem
        fields = ['name', 'travel', 'id']


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['address', 'date', 'hour',
                  'notes', 'price', 'type_card', 'latitude', 'longitude', 'travel', 'id']


class AccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = ['address', 'check_in_date', 'check_in_hour',
                  'check_out_date', 'check_out_hour', 'price', 'type_card', 'latitude', 'longitude', 'travel', 'id']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['address', 'check_in_date', 'check_in_hour',
                  'seat', 'boarding_gate', 'price', 'type_card', 'latitude', 'longitude', 'travel', 'id']
