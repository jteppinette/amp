"""
This module defines the Admin pages for the new `User` model.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from authentication.models import User
from authentication.forms import UserCreationForm, UserChangeForm


class CustomUserAdmin(UserAdmin):
    """
    The forms to add and change user instances.
    """
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'company', 'title', 'is_admin', 'is_active')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('AMP Information', {'fields': ('first_name', 'last_name', 'company', 'title')}),
        ('Change Password', {'fields': ('new_password',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )

    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('email', 'first_name', 'last_name', 'company', 'title', 'password1', 'password2')}),
    )

    search_fields = ('email',)
    ordering = ('company', 'email')
    filter_horizontal = ()


# Register admin class with the admin app.
admin.site.register(User, CustomUserAdmin)

# Unregister `Group` from the admin app.
admin.site.unregister(Group)
