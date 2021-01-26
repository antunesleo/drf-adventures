from django.contrib import admin
from django.urls import path, include

from drfadventures import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.api_root),
    path('', include('sharethoughts.urls')),
    path('', include('iam.urls'))
]
