from django.contrib import admin
from appAPI.models import MyUser
from django.contrib.auth.admin import UserAdmin

class SuperUser(UserAdmin):
    # Customize the fields shown in the user list page for superusers
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active']

    # Customize the fields shown on the user detail page for superusers
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'user_permissions')}),
        # Add any other custom fieldsets here
    )

# Register your models here.

admin.site.register(MyUser, SuperUser)
