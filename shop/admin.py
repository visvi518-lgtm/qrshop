from django.contrib import admin
from .models import Customer, Receiver, Order

class ReceiverInline(admin.TabularInline):
    model = Receiver
    extra = 0

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "address")
    search_fields = ("name", "phone")
    inlines = [ReceiverInline]

@admin.register(Receiver)
class ReceiverAdmin(admin.ModelAdmin):
    list_display = ("customer", "name", "phone", "address")
    search_fields = ("name", "phone", "customer__name", "customer__phone")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("created_at", "customer", "product", "quantity", "total_price")
    search_fields = ("customer__name", "customer__phone", "product")
    list_select_related = ("customer",)
