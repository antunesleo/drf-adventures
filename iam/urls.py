from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt import views as jwt_views

from iam.views import UserListViewSet, UserDetailViewSet

router = DefaultRouter()
router.register(r'api/users', UserListViewSet)
router.register(r'api/users', UserDetailViewSet)

urlpatterns = [
    path('', include(router.urls))
]

urlpatterns += format_suffix_patterns([
    path(
        'api/token',
        jwt_views.TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/token/refresh',
        jwt_views.TokenRefreshView.as_view(),
        name='token_refresh'
    )
])
