from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("created_at", "name", "phone", "product_name", "quantity")
    search_fields = ("name", "phone", "product_name")
    list_filter = ("created_at",)
