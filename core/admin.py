# accounts/admin.py

from django.contrib import admin
from .models import LoginIPAddress


@admin.register(LoginIPAddress)
class LoginIPAddressAdmin(admin.ModelAdmin):
    list_display = ("user", "last_login_ip")
    search_fields = ("user__username", "last_login_ip")
