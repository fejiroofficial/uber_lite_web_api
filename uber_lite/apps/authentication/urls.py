from django.urls import path
from .views import RegisterUsers, ActivateUser


urlpatterns = [
    path('auth/register/', RegisterUsers.as_view(), name="auth-register"),
    path('auth/register/activate',
         ActivateUser.as_view(),
         name="activate-user")
]
