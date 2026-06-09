from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ('email',)
    list_display = ('email', 'prenom', 'nom', 'niveau', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'niveau', 'filiere')
    search_fields = ('email', 'prenom', 'nom', 'telephone')
    readonly_fields = ('date_inscription', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {
            'fields': ('prenom', 'nom', 'telephone', 'niveau', 'filiere', 'bio', 'photo', 'centre_interet'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Dates', {'fields': ('last_login', 'date_inscription')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2',
                'prenom', 'nom', 'telephone', 'niveau', 'filiere',
            ),
        }),
    )
