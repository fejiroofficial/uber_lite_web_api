from django.urls import path
from .views import RegisterUsers


urlpatterns = [
    path('auth/register/', RegisterUsers.as_view(), name="auth-register")
]
