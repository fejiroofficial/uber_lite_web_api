from django.db import models
from django.contrib.auth.models import (PermissionsMixin, AbstractBaseUser,
                                        BaseUserManager)
from phone_field import PhoneField
from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class UserManager(BaseUserManager):
    def create_user(self, is_driver, **kwargs):
        email = kwargs.get('email')
        first_name = kwargs.get('first_name')
        last_name = kwargs.get('last_name')
        telephone = kwargs.get('telephone')
        activation_code = kwargs.get('activation_code')
        password = kwargs.get('password')
        license_number = kwargs.get('license_number')
        driver_license_image = kwargs.get(
            'driver_license_image')

        user = self.model(email=email,
                          first_name=first_name,
                          last_name=last_name,
                          telephone=telephone,
                          activation_code=activation_code,
                          password=password)
        user.set_password(password)
        user.is_active = False
        user.is_superuser = False

        if is_driver:
            user.is_driver = True
            user.save()

            driver_profile = DriverProfile.objects.create(user=user)
            if license_number:
                driver_profile.license_number = license_number
            if driver_license_image:
                driver_profile.driver_license_image = driver_license_image
            driver_profile.save()
            return user

        user.save()
        return user

    def create_superuser(self, **kwargs):
        email = kwargs.get('email')
        first_name = kwargs.get('first_name')
        last_name = kwargs.get('last_name')
        telephone = kwargs.get('telephone')
        activation_code = kwargs.get('activation_code')
        password = kwargs.get('password')
        user = self.model(email=email,
                          first_name=first_name,
                          last_name=last_name,
                          telephone=telephone,
                          activation_code=activation_code,
                          password=password)
        user.set_password(password)
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email_):
        return self.get(email=email_)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    telephone = PhoneField(unique=True, help_text='Contact phone number')
    activation_code = models.IntegerField()
    profile_image = models.URLField(
        default=getenv('PLACEHOLDER_IMAGE')
    )
    is_active = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_short_name(self):
        return self.first_name

    def natural_key(self):
        return self.email

    def __str__(self):
        return self.email


class DriverProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True)
    license_number = models.CharField(max_length=50)
    driver_license_image = models.URLField(
        default=getenv('PLACEHOLDER_IMAGE'))
