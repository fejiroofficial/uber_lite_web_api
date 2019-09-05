from django.urls import path
from .views import RegisterUsers, ActivateUser, LoginUsers


urlpatterns = [
    path('auth/register/', RegisterUsers.as_view(), name="auth-register"),
    path('auth/register/activate',
         ActivateUser.as_view(),
         name="activate-user"),
    path('auth/login/', LoginUsers.as_view(), name="users/login")
]
