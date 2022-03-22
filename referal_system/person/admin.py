"""person application Admin Settings"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User, Invite, Code


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        ('Personal info', {'fields': ('phone_number', 'invite_code',
         'is_active', 'is_superuser')}),
        ('Groups, permissions', {
            'fields': ('groups', 'user_permissions'),
        })
        )

    list_display = ('phone_number', 'invite_code', 'is_active')
    search_fields = ('phone_number', 'invite_code')
    ordering = ('phone_number', 'invite_code')


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ('owner', 'invited')
    search_fields = ('owner', 'invited')
    ordering = ('owner', 'invited')


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ('person', 'code')
    search_fields = ('person', 'code')
    ordering = ('person', 'code')
