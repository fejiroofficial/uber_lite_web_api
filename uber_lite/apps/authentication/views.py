import random
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import status
from .models import CustomUser
from uber_lite.utils.auth_sms import send_sms
from .validator import validate_signup


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

        new_user = CustomUser.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            password=password,
            email=email,
            telephone=telephone,
            activation_code=self.activation_code,
        )

        message = f'<#> {new_user.activation_code}' \
            ' is your Uberlite activation code.'
        telephone_number = new_user.telephone
        send_sms(telephone_number, message)
        return Response(
            data={
                'userId': new_user.id,
                'message': 'Thank you for choosing uberlite!'
                           ' An activation code'
                           ' has been sent to the telephone'
                           ' number you provided',
            },
            status=status.HTTP_201_CREATED
        )
