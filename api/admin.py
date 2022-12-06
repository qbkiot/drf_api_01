from django.contrib import admin
from .models import Item, Pet, Reminder

# Register your models here.
admin.site.register(Reminder)
admin.site.register(Pet)
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    list_filter = ['created',]