from django.db import models
import uuid
from django.utils import timezone

# Create your models here.
"""
Model for test case
"""
class Item(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    name = models.CharField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class SubItem(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    name = models.CharField(max_length=200, unique=False)
    created = models.DateTimeField(auto_now_add=True)

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='subitems', blank=True, null=True)

    def __str__(self):
        return self.name

"""
Model for user
"""
class User(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.id

"""
Models for Bouwl app api
->when complete delete Item/SubItem and swap
"""
class Pet(models.Model):
    #owner = 
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    desc = models.CharField(max_length=30)
    photo = models.ImageField(blank=True)
    birthdate = models.DateField(default=timezone.now, blank=True) 
    icon = models.CharField(max_length=30, default="pawprint")
    color = models.CharField(max_length=30, default="AFC-blue")

    def __str__(self):
        return self.name

class Reminder(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4, editable = False)
    name = models.CharField(max_length=100)
    completion = models.BooleanField(default=False)
    icon = models.CharField(max_length=30, default="exclamationmark.circle")
    type = models.CharField(max_length=30)
    date = models.DateField(default=timezone.now)
    desc = models.CharField(max_length=250)

    pet=models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='reminders', blank=True, null=True)
    
    def __str__(self):
        return self.name