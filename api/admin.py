from django.contrib import admin
from .models import Item #, User

# Register your models here.

#admin.site.register(User)
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    list_filter = ['created']


