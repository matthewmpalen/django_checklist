# Django
from django.contrib import admin

# Local
from .models import Checklist, Item

class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at', 'updated_at')
    list_filter = ('user',)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('checklist', 'description', 'is_complete', 'created_at', 
        'updated_at')
    list_filter = ('checklist', 'is_complete')

admin.site.register(Checklist, ChecklistAdmin)
admin.site.register(Item, ItemAdmin)
