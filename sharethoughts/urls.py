from django.urls import path

from sharethoughts.views import ThoughtListView, ThoughtDetailView

urlpatterns = [
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
]
