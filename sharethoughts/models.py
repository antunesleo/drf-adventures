from django.db import models

# Create your models here.


class Thought(models.Model):
    thought = models.CharField(max_length=800)
    created_at = models.DateTimeField(auto_now_add=True)
