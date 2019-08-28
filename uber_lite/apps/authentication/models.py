from django.db import models
from django.contrib.auth.models import (PermissionsMixin, AbstractBaseUser,
                                        BaseUserManager)
from phone_field import PhoneField


class CustomUserManager(BaseUserManager):
    def create_user(self, **kwargs):
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
        user.is_active = False
        user.is_superuser = False
        user.save(using=self._db)
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
        default='https://res.cloudinary.com/health-id/image/upload/'
        'v1554552278/Profile_Picture_Placeholder.png'
    )
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_short_name(self):
        return self.first_name

    def natural_key(self):
        return self.email

    def __str__(self):
        return self.email
