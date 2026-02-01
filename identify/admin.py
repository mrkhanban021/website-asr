from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Profile




class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'پروفایل کاربر'
    fk_name = 'user'
    readonly_fields = ('created_time', 'updated_time')
    extra = 0  





@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    ordering = ['-is_superuser', '-is_active']
    
    list_display = [
        'email', 'created_time', 'updated_time',
        'is_active', 'is_staff', 'is_superuser'
    ]
    

    search_fields = ['email']
    
  
    list_filter = ['is_active', 'is_staff', 'is_superuser']
    

    fieldsets = (
        (None, {'fields': ('id','email', 'password')}),
        ('دسترسی‌ها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('زمان‌بندی', {'fields': ('created_time', 'updated_time')}),
    )

 
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')
        }),
    )
    readonly_fields = ('created_time', 'updated_time', 'id')

    inlines = [ProfileInline]

    exclude = ('username',)
