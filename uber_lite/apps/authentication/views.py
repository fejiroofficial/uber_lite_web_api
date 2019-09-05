import random

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login

from rest_framework_jwt.settings import api_settings
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import status

from .models import CustomUser
from uber_lite.utils.auth_sms import send_sms
from .validator import validate_signup
from .serializers import (UserSerializer,
                          ActivateUserSerializer,
                          TokenSerializer)


# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class RegisterUsers(generics.CreateAPIView):
    """
    POST auth/register/
    """
    permission_classes = (AllowAny,)
    activation_code = random.randint(1000, 9999)

    @validate_signup
    def post(self, request, *args, **kwargs):
        firstname = request.data.get('firstname', '').strip()
        lastname = request.data.get('lastname', '').strip()
        email = request.data.get('email', '').strip()
        telephone = request.data.get('telephone', '').strip()
        password = request.data.get('password', '').strip()

        serializer = UserSerializer(data={
            'first_name': firstname,
            'last_name': lastname,
            'password': password,
            'email': email,
            'telephone': telephone,
            'activation_code': self.activation_code,
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()

        message = f'<#> {serializer.data["activation_code"]}' \
            ' is your Uberlite activation code.'
        telephone_number = serializer.data['telephone']
        send_sms(telephone_number, message)
        return Response(
            data={
                'message': 'Thank you for choosing uberlite!'
                           ' An activation code'
                           ' has been sent to the telephone'
                           ' number you provided',
            },
            status=status.HTTP_201_CREATED
        )


class ActivateUser(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    queryset = CustomUser.objects.all()

    def patch(self, request, *args, **kwargs):
        activation_code = request.data.get('activation_code',
                                           '').strip().replace(' ', '')

        user = None

        try:
            user = self.queryset.get(activation_code=activation_code,
                                     is_active=False)
        except (ObjectDoesNotExist, ValueError):
            return Response(
                data={
                    'message': 'INVALID Activation code!!!'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ActivateUserSerializer(
            instance=user,
            data={
                'is_active': True
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        token_serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
        token_serializer.is_valid()
        return Response(
            data={
                'message': 'This account has been successfully activated',
                'token': token_serializer.data['token']
            },
            status=status.HTTP_200_OK
        )


class LoginUsers(generics.CreateAPIView):
    """
    POST auth/login
    """
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email',
                                 '').strip().replace(' ', '')
        password = request.data.get('password',
                                    '').strip().replace(' ', '')

        u_user = CustomUser.objects.filter(email=email).first()
        print('jndqd', u_user.is_active)
        user = authenticate(request, username=email, password=password)
        print('user :', user, email, password)
        if user:
            login(request, user)
            serializer = TokenSerializer(data={
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(
                data={
                    'message': 'Login successfully',
                    'token': serializer.data['token']
                },
                status=status.HTTP_200_OK
            )
        return Response(
            data={
                'message': 'Email/password combination incorrect'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
