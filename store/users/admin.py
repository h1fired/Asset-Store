from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):

    list_display = ('email', 'username', 'is_staff', 'is_superuser', 'is_verified', 'is_active')
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'is_verified', 'password')}),
        ('Groups', {'fields': ('groups',)}),
        ('Personal Info', {'fields': ('username', 'picture',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'is_verified', 'password1', 'password2')}),
        ('Groups', {'fields': ('groups',)}),
        ('Personal Info', {'fields': ('username', 'picture',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    search_fields = ('email', )
    ordering = ('email',)
    filter_horizontal = ()
    
admin.site.register(CustomUser, CustomUserAdmin)