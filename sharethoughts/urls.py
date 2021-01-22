from rest_framework.routers import DefaultRouter
from sharethoughts.views import ThoughtViewSet

router = DefaultRouter()
router.register(r'thoughts', ThoughtViewSet)
urlpatterns = router.urls
