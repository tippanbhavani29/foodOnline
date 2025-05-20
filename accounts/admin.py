from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User, UserProfile
class CustomUserAdmin(UserAdmin):
    list_display=('first_name','last_name','username','role','is_active')
    ordering = ('-date_joinied',)
    filter_horizontal=()
    list_filter=()
    fieldsets=()

admin.site.register(User,CustomUserAdmin)
admin.site.register(UserProfile)