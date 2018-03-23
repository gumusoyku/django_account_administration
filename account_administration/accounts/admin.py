from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "IBAN")
    search_fields = ("first_name", "last_name")

