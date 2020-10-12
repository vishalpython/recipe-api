from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from recipe_api import models
from django.utils.translation import gettext as _

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
    (None, {'fields': ('email', 'password')}),
    (('personal Info',), {'fields': ('name',)}),
    (('permissions'),
      {'fields': ('is_active', 'is_staff', 'is_superuser')}
    ),
    (('Important date'),{'fields': ('last_login',)})
    )
    add_fieldsets = (
    (None,
    {
    'classes':('wide',),
    'fields':('email', 'password1','password2')
    }),
    )

admin.site.register(models.User, UserAdmin)
