import json
from mock import patch

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from uber_lite.apps.authentication.models import CustomUser


# test models
class CustomUserModelTest(APITestCase):
    def setUp(self):
        self.a_user = CustomUser.objects.create(
            first_name='fyoyo',
            last_name='lyoyo',
            email='yoyo@gmail.com',
            telephone='+2348138776199',
            password='12345678',
            activation_code=5091,
        )

    def test_custom_user(self):
        """
        This test ensures that the user created in the setup
        exist
        """
        self.assertEqual(self.a_user.first_name, 'fyoyo')
        self.assertEqual(self.a_user.last_name, 'lyoyo')
        self.assertEqual(self.a_user.email, 'yoyo@gmail.com')
        self.assertEqual(self.a_user.telephone, '+2348138776199')
        self.assertEqual(self.a_user.activation_code, 5091)


# test views
class BaseViewTest(APITestCase):
    client = APIClient()

    def register_a_user(self, **kwargs):
        return self.client.post(
            path='/api/v1/auth/register/',
            data=json.dumps(kwargs),
            content_type='application/json'
        )

    def activate_a_user(self, **kwargs):
        return self.client.patch(
            path='/api/v1/auth/register/activate',
            data=json.dumps(kwargs),
            content_type='application/json'
        )


class AuthRegisterUserTest(BaseViewTest):

    def setUp(self):
        self.a_user = CustomUser.objects.create(
            first_name='fyoyo',
            last_name='lyoyo',
            email='yoyo@gmail.com',
            telephone='+2348138776199',
            password='12345678',
            activation_code=5091,
        )

    """
    Tests for auth/register/ endpoint
    """
    @patch('uber_lite.apps.authentication.views.send_sms')
    def test_register_a_user(self, mock):
        response = self.register_a_user(
                    firstname="user_firstname",
                    lastname="user_lastname",
                    email="new_user@mail.com",
                    telephone="+2348140506231",
                    password="12345678")
        self.assertEqual(response.data["message"],
                         'Thank you for choosing uberlite! '
                         'An activation code has been sent '
                         'to the telephone number you provided')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # test with invalid data
        response = self.register_a_user()
        # assert status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activate_user(self):
        response = self.activate_a_user(
            activation_code='5091'
        )
        self.assertEqual(response.data["message"],
                         'This account has been successfully activated')
