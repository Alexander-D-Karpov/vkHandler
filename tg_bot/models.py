from django.db import models
from callback.models import Tag, Post


# Create your models here.


class User(models.Model):
    uuid = models.IntegerField(primary_key=True, blank=False)
    username = models.CharField(max_length=100)
    joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.uuid)


class UserTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.tag.name + " - " + self.user.username


class UserAttend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " - " + self.post.text[:50]
