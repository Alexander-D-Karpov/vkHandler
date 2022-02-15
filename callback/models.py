from django.db import models


class Post(models.Model):
    text = models.TextField()
    event_id = models.CharField(max_length=100, unique=True)
    date = models.DateField(blank=True, null=True)
    link = models.URLField()

    def __str__(self):
        return self.text[:100]


class Tag(models.Model):
    name = models.CharField(max_length=50)
    tags = models.TextField(blank=False)

    def __str__(self):
        return self.name


class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return self.post.text[:50] + " - " + self.tag.name
