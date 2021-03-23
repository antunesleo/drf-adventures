from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from thoughts.hashtags import unique_hashtags


class Thought(models.Model):
    owner = models.ForeignKey(
        'auth.User',
        editable=False,
        on_delete=models.CASCADE
    )
    thought = models.TextField(max_length=800, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.thought


class Hashtag(models.Model):
    creator = models.ForeignKey(
        'auth.User',
        editable=False,
        on_delete=models.SET_NULL,
        null=True
    )
    hashtag = models.TextField(max_length=100, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    thoughts = models.ManyToManyField(Thought)


@receiver(post_save, sender=Thought)
def register_thought_hashtags(sender, created, instance, **kwargs):
    if created:
        hashtags = unique_hashtags(instance.thought)
        for hashtag in hashtags:
            try:
                hashtag_model = Hashtag.objects.get(hashtag=hashtag)
            except ObjectDoesNotExist:
                hashtag_model = Hashtag(hashtag=hashtag, creator=instance.owner)
                hashtag_model.save()

            hashtag_model.thoughts.add(instance)
            hashtag_model.save()
    print('Houston, we have a problem')
