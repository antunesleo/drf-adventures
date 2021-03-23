from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from thoughts.views import ThoughtListView, ThoughtDetailView


urlpatterns = format_suffix_patterns([
    path(
        'api/thoughts',
        ThoughtListView.as_view(),
        name='thought-list'
    ),
    path(
        'api/thoughts/<int:pk>/',
        ThoughtDetailView.as_view(),
        name='thought-detail'
    )
])
