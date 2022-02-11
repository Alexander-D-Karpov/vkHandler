from django.db import models


class Post(models.Model):
    object = models.JSONField()
    event_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.object['text']


class Tag(models.Model):
    name = models.CharField(max_length=50)
    tags = models.TextField(blank=False)

    def __str__(self):
        return self.name
