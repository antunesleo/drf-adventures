from django.urls import path

from sharethoughts.views import ThoughtListView

urlpatterns = [
    path(
        'thoughts',
        ThoughtListView.as_view(),
        name='thought-list'
    )
]
