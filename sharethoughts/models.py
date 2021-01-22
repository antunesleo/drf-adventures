from django.db import models


class Thought(models.Model):
    thought = models.TextField(max_length=800)
    created_at = models.DateTimeField(auto_now_add=True)
