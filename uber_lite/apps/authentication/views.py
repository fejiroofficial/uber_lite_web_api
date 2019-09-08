import random

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login

from rest_framework_jwt.settings import api_settings
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import status

from uber_lite.utils.messages import authentication as auth_messages
from uber_lite.utils.request_helpers import get_request_param
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
        firstname = get_request_param(request, 'firstname')
        lastname = get_request_param(request, 'lastname')
        email = get_request_param(request, 'email')
        telephone = get_request_param(request, 'telephone')
        password = get_request_param(request, 'password')
        license_number = get_request_param(request, 'license_number')

        serializer = UserSerializer(data={
            'first_name': firstname,
            'last_name': lastname,
            'password': password,
            'email': email,
            'telephone': telephone,
            'license_number': license_number,
            'is_driver': kwargs.get('is_driver'),
            'activation_code': self.activation_code,
        })
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        account_type = 'Driver' if user.is_driver else 'User'

        message = auth_messages.SUCCESS['ACTIVATION_SMS_TEXT'].format(
            serializer.data["activation_code"], account_type)

        telephone_number = serializer.data['telephone']
        # send_sms(telephone_number, message)
        return Response(
            data={
                'message': auth_messages.SUCCESS['SIGN_UP'].format(
                    account_type),
            },
            status=status.HTTP_201_CREATED)


class ActivateUser(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    queryset = CustomUser.objects.all()

    def patch(self, request, *args, **kwargs):
        activation_code = get_request_param(
            request, 'activation_code').replace(' ', '')

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
                'message': auth_messages.SUCCESS['ACCOUNT_ACTIVATION'],
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
        email = get_request_param(request, 'email').replace(' ', '')
        password = get_request_param(request, 'password').replace(' ', '')

        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            serializer = TokenSerializer(data={
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(
                data={
                    'message': auth_messages.SUCCESS['LOGIN'],
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
