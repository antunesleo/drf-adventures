from django.urls import path

from sharethoughts.views import ThoughtListView, ThoughtDetailView

urlpatterns = [
    path(
        'thoughts',
        ThoughtListView.as_view(),
        name='thought-list'
    ),
    path(
        'thoughts/<int:pk>/',
        ThoughtDetailView.as_view(),
        name='thought-detail'
    )
]
