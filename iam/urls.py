from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from iam.views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path(
        'api/token',
        jwt_views.TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/token/refresh',
        jwt_views.TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path('', include(router.urls))
]
