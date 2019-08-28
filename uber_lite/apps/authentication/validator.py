from rest_framework.response import Response
from rest_framework.views import status
from .models import CustomUser


def validate_signup(func):
    def wrapper(*args, **kwargs):
        errors = []
        REQUIRED_FIELDS = ['firstname',
                           'lastname',
                           'email',
                           'telephone',
                           'password']
        for field in REQUIRED_FIELDS:
            if field not in args[0].request.data:
                errors.append(f'{field} is required but none provided')

        if errors:
            return Response(
                data={
                    'message': errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        email = args[0].request.data.get('email', '')
        telephone = args[0].request.data.get('telephone', '')

        email_exist = CustomUser.objects.filter(
            email=email
        ).first()

        telephone_exist = CustomUser.objects.filter(
            telephone=telephone
        ).first()

        if email_exist:
            return Response(
                data={
                    'message': 'A user with this email {email} '
                               'already exist'.format(email=email)
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        if telephone_exist:
            return Response(
                data={
                    'message': 'A user with this mobile number {telephone} '
                    'already exist'.format(telephone=telephone)
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        return func(*args, **kwargs)
    return wrapper
