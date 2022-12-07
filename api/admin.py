from django.contrib import admin
from .models import Item, SubItem, Pet, Reminder

# Register your models here.
admin.site.register(Reminder)
admin.site.register(Pet)
#admin.site.register(SubItem)
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    list_filter = ['created',]

@admin.register(SubItem)
class SubItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'id','created']
    list_filter = ['created',]