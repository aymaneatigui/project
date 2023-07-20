from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField()
    pwd = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.username