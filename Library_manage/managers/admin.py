from django.contrib import admin
from account.models import User
from .models import SystemSettings, UserRole

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login')
    list_filter = ('is_superuser', 'is_staff', 'is_active', 'role', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'address')
    readonly_fields = ('date_joined', 'last_login')
    list_per_page = 25
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'role', 'phone_number', 'address', 'date_of_birth', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Library Info', {'fields': ('fine_balance',)}),
    )

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at', 'updated_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ('review_system_enabled', 'google_books_api_enabled', 'last_backup', 'maintenance_scheduled')
    readonly_fields = ('last_backup',)
    fieldsets = (
        (None, {'fields': ('review_system_enabled', 'google_books_api_enabled')}),
        ('Maintenance', {'fields': ('maintenance_scheduled', 'maintenance_message')}),
        ('System Info', {'fields': ('last_backup',)}),
    )
