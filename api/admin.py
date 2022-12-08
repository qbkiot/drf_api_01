from django.contrib import admin
from .models import Item, SubItem, Pet, Reminder, MyUser

@admin.register(Pet)
class PetAdmis(admin.ModelAdmin):
    list_display = ['name', 'id', 'owner']
    list_filter = ['owner',]

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'pet']
    list_filter = ['pet',]
@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'id', 'password']
    
"""
# old item,subitem admin registration
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    list_filter = ['created',]

@admin.register(SubItem)
class SubItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'id','created']
    list_filter = ['created',]
"""