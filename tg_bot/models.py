from django.db import models

# Create your models here.


class User(models.Model):
    uuid = models.IntegerField(primary_key=True, blank=False)
    username = models.CharField(max_length=100)
    joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.uuid)


class UserTag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name + " - " + str(self.user.uuid)

