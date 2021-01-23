from django.db import models


class Thought(models.Model):
    owner = models.ForeignKey(
        'auth.User',
        editable=False,
        on_delete=models.CASCADE
    )
    thought = models.TextField(max_length=800, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
