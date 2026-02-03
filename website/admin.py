from django.contrib import admin
from .models import SiteSetting
# Register your models here.


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'phone_factory', 'email', 'created_time')
    list_filter = ('site_name',)
    search_fields = ('site_name',)