from django.db import models
import uuid
from django.utils import timezone

# Create your models here.

class Item(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    name = models.CharField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class User(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.id


"""

Models for Bouwl app api
->delete Item and swap

"""
class Pet(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    desc = models.CharField(max_length=30)
    photo = models.ImageField(blank=True)
    birthdate = models.DateField(default=timezone.now, blank=True) 
    icon = models.CharField(max_length=30, default="pawprint")
    color = models.CharField(max_length=30, default="AFC-blue")
    
    def __str__(self):
        return self.id

class Reminder(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    name = models.CharField(max_length=100)
    completion = models.BooleanField(default=False)
    icon = models.CharField(max_length=30, default="exclamationmark.circle")
    type = models.CharField(max_length=30)
    date = models.DateField(default=timezone.now)
    desc = models.CharField(max_length=250)
    
    # One to many relation
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    def __str__(self):
        
        return self.id