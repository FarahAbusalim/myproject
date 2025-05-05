from django.contrib import admin
from .models import Advertisement
# Register your models here.

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

admin.site.register(Advertisement, AdvertisementAdmin)

