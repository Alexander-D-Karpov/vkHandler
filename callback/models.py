from django.db import models


class Post(models.Model):
    text = models.TextField()
    event_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.text


class Tag(models.Model):
    name = models.CharField(max_length=50)
    tags = models.TextField(blank=False)

    def __str__(self):
        return self.name


class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)