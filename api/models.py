from django.db import models
import uuid
# Create your models here.

class Item(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    name = models.CharField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    login = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.id