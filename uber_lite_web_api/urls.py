from django.contrib import admin
from django.urls import path, include
from uber_lite_web_api.views import BaseView

urlpatterns = [
    path('', BaseView.as_view(), name='base_url'),
    # path('api/v1', include('apps.authentication.urls')),
    path('admin/', admin.site.urls)
]
