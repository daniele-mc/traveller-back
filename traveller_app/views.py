from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser


class LoginUserView(APIView):
    def post(self, request, *args, **kwargs):
        users = User.objects.filter(username=request.data['username'])

        if not users.exists():
            data = {
                'error': 'Usuário não encontrado.'
            }
            return Response(data, status=400)

        user = users.first()

        if not user.check_password(request.data['password']):
            data = {
                'error': 'Senha incorreta.'
            }
            return Response(data, status=400)

        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key
        }

        return Response(data, status=201)


class RegisterUserView(APIView):
    def post(self, request, *args, **kwargs):
        data_serializer = UserSerializer(data=request.data)

        if data_serializer.is_valid():
            data_serializer.save()
            return Response(data_serializer.data, status=201)
        else:
            return Response(data_serializer.errors, status=400)


class GetUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data_serializer = UserSerializer(request.user).data

        return Response(data_serializer, status=200)

    def patch(self, request, *args, **kwargs):
        data_serializer = UserSerializer(request.user, data=request.data)
        if data_serializer.is_valid():
            data_serializer.save()
            return Response(data_serializer.data, status=201)
        else:
            return Response(data_serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        request.user.delete()
        return Response(status=204)


class GetPhotoView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, )

    def get(self, request, *args, **kwargs):
        if hasattr(request.user, 'extrauser'):
            data = ExtraUserSerializer(request.user.extrauser).data
            return Response(data, status=200)
        else:
            data = {
                'error': 'Não possui foto'
            }
            return Response(data, status=400)

    def post(self, request, *args, **kwargs):
        new_data = {
            'photo': request.data['photo'],
            'user': request.user.id
        }
        if hasattr(request.user, 'extrauser'):
            data_serializer = ExtraUserSerializer(
                request.user.extrauser, data=new_data)
        else:
            data_serializer = ExtraUserSerializer(data=new_data)

        if data_serializer.is_valid():
            data_serializer.save()
            return Response(data_serializer.data, status=201)
        else:
            return Response(data_serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        request.user.extrauser.delete()
        return Response(status=204)


class CreateTravelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        new_data = {
            **request.data,
            "user": request.user.id,
            "active": True
        }
        data_serializer = TravelSerializer(data=new_data)

        if data_serializer.is_valid():
            data_serializer.save()
            return Response(data_serializer.data, status=201)
        else:
            return Response(data_serializer.errors, status=400)


class TravelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        travels = Travel.objects.filter(user=request.user, active=True)
        travel = travels.first()

        data_serializer = TravelSerializer(travel).data
        return Response(data_serializer, status=200)

    def patch(self, request, *args, **kwargs):
        travels = Travel.objects.filter(user=request.user, active=True)
        travel = travels.first()

        new_data = {
            **request.data,
            "user": request.user.id,
            "active": True
        }
        data_serializer = TravelSerializer(travel, data=new_data)

        if data_serializer.is_valid():
            data_serializer.save()
            return Response(data_serializer.data, status=201)
        else:
            return Response(data_serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        travels = Travel.objects.filter(user=request.user, active=True)
        travel = travels.first()

        travel.delete()
        return Response(status=204)


class TravelInactiveView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        print(request)
        travels = Travel.objects.filter(user=request.user, active=True)
        travel = travels.first()

        travel.active = False
        travel.save()
        return Response(status=201)


class GetAllTravelsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        travels = Travel.objects.filter(user=request.user)
        data_serializer = TravelSerializer(travels, many=True).data
        return Response(data_serializer, status=200)


class CreateRouteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        travels = Travel.objects.filter(user=request.user, active=True)
        travel = travels.first()
        new_data = {
            **request.data,
            "travel": travel.id,
        }
        data_serializer = RouteSerializer(data=new_data)
        if data_serializer.is_valid():
            data_serializer.save()
            return Response(data_serializer.data, status=201)
        else:
            return Response(data_serializer.errors, status=400)


class RouteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        route = Route.objects.get(id=kwargs['id'])

        data_serializer = RouteSerializer(route).data

        return Response(data_serializer, status=200)

    def patch(self, request, *args, **kwargs):
        route = Route.objects.get(id=kwargs['id'])
        travels = Travel.objects.filter(user=request.user, active=True)
        travel = travels.first()
        new_data = {
            **request.data,
            "travel": travel.id,
        }
        data_serializer = RouteSerializer(route, data=new_data)

        if data_serializer.is_valid():
            data_serializer.save()
            return Response(data_serializer.data, status=201)
        else:
            return Response(data_serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        route = Route.objects.get(id=kwargs['id'])
        route.delete()

        return Response(status=204)


class CreateAccommodationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        travels = Travel.objects.filter(user=request.user, active=True)
        travel = travels.first()
        new_data = {
            **request.data,
            "travel": travel.id,
        }
        data_serializer = AccommodationSerializer(data=new_data)

        if data_serializer.is_valid():
            data_serializer.save()
            return Response(data_serializer.data, status=201)
        else:
            return Response(data_serializer.errors, status=400)


class AccommodationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        accommodation = Accommodation.objects.get(id=kwargs['id'])

        data_serializer = AccommodationSerializer(accommodation).data

        return Response(data_serializer, status=200)

    def patch(self, request, *args, **kwargs):
        accommodation = Accommodation.objects.get(id=kwargs['id'])
        travels = Travel.objects.filter(user=request.user, active=True)
        travel = travels.first()
        new_data = {
            **request.data,
            "travel": travel.id,
        }
        data_serializer = AccommodationSerializer(
            accommodation, data=new_data)

        if data_serializer.is_valid():
            data_serializer.save()
            return Response(data_serializer.data, status=201)
        else:
            return Response(data_serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        accommodation = Accommodation.objects.get(id=kwargs['id'])
        accommodation.delete()

        return Response(status=204)


class CreateTicketView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        travels = Travel.objects.filter(user=request.user, active=True)
        travel = travels.first()
        new_data = {
            **request.data,
            "travel": travel.id,
        }
        data_serializer = TicketSerializer(data=new_data)

        if data_serializer.is_valid():
            data_serializer.save()
            return Response(data_serializer.data, status=201)
        else:
            return Response(data_serializer.errors, status=400)


class TicketView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        ticket = Ticket.objects.get(id=kwargs['id'])

        data_serializer = TicketSerializer(ticket).data

        return Response(data_serializer, status=200)

    def patch(self, request, *args, **kwargs):
        ticket = Ticket.objects.get(id=kwargs['id'])
        travels = Travel.objects.filter(user=request.user, active=True)
        travel = travels.first()
        new_data = {
            **request.data,
            "travel": travel.id,
        }
        data_serializer = TicketSerializer(ticket, data=new_data)

        if data_serializer.is_valid():
            data_serializer.save()
            return Response(data_serializer.data, status=201)
        else:
            return Response(data_serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        ticket = Ticket.objects.get(id=kwargs['id'])
        ticket.delete()

        return Response(status=204)


class CreateBackpackItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        travels = Travel.objects.filter(user=request.user, active=True)
        travel = travels.first()
        new_data = {
            **request.data,
            "travel": travel.id,
        }
        data_serializer = BackpackItemSerializer(data=new_data)

        if data_serializer.is_valid():
            data_serializer.save()
            return Response(data_serializer.data, status=201)
        else:
            return Response(data_serializer.errors, status=400)


class BackpackItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        backpack_item = BackpackItem.objects.get(id=kwargs['id'])

        data_serializer = BackpackItemSerializer(backpack_item).data

        return Response(data_serializer, status=200)

    def patch(self, request, *args, **kwargs):
        backpack_item = BackpackItem.objects.get(id=kwargs['id'])
        travels = Travel.objects.filter(user=request.user, active=True)
        travel = travels.first()
        new_data = {
            **request.data,
            "travel": travel.id,
        }
        data_serializer = BackpackItemSerializer(
            backpack_item, data=new_data)

        if data_serializer.is_valid():
            data_serializer.save()
            return Response(data_serializer.data, status=201)
        else:
            return Response(data_serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        backpack_item = BackpackItem.objects.get(id=kwargs['id'])
        backpack_item.delete()

        return Response(status=204)
