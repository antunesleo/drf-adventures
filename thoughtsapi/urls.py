from django.contrib import admin
from django.urls import path, include

from thoughtsapi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.api_root),
    path('', include('thoughts.urls')),
    path('', include('iam.urls'))
]
