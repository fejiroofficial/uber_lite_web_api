from django.contrib import admin
from django.urls import path, include, re_path
from uber_lite.views import BaseView

urlpatterns = [
    path('', BaseView.as_view(), name='base_url'),
    # path(r'^api/', include('rest_framework_simplejwt.urls')),
    path('admin/', admin.site.urls),
    re_path('api/v1/', include('uber_lite.apps.authentication.urls')),
]
