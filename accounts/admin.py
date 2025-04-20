from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users

class CustomUserAdmin(UserAdmin):
     model = Users
     list_display = ('email', 'last_name', 'id')
     list_filter = ('is_staff', 'is_active')
     search_fields = ('email', 'first_name', 'last_name', 'id', 'user_name')
     ordering = ('email',)
     readonly_fields = ('date_joined', 'last_login')
     fieldsets = (
         (None, {'fields': ('email', 'password')}),
         ('User Information', {'fields': ('first_name', 'last_name','user_name','avatar')}),
         ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions', 'role')}),
         ('Important dates', {'fields': ('date_joined', 'last_login')})
     )
     add_fieldsets = (
         (None, {
             'classes': ('wide',),
             'fields': ('email', 'first_name', 'last_name', 'user_name', 'password1', 'password2')}
         ),
     )

admin.site.register(Users, CustomUserAdmin)
