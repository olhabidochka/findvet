from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'created_at']
    fieldsets = UserAdmin.fieldsets + (
        ('Додаткова інформація', {'fields': ('role', 'phone', 'address', 'avatar', 'date_of_birth')}),
    )