from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


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
