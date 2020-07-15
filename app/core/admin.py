from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseAdmin):
    """ custom user admin """
    ordering = ['id']
    list_display = ['id', 'email', 'name', 'about', 'age', 'exp']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('User Info'), {'fields': ('about', 'age', 'exp')}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important Dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'name', 'email', 'password1', 'password2', 'about', 'age'
            )
        }),
    )


admin.site.register(models.User, UserAdmin)