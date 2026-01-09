# orders/admin.py
from django.contrib import admin
from django.http import HttpResponse
from openpyxl import Workbook

from .models import Order  # 네 모델명에 맞게

@admin.action(description="엑셀(.xlsx) 다운로드")
def export_orders_to_xlsx(modeladmin, request, queryset):
    wb = Workbook()
    ws = wb.active
    ws.title = "orders"

    # 헤더 (네 필드에 맞게 수정 가능)
    ws.append(["created_at", "name", "phone", "product_name", "quantity"])

    for o in queryset.order_by("-created_at"):
        ws.append([
            o.created_at.strftime("%Y-%m-%d %H:%M:%S") if o.created_at else "",
            getattr(o, "name", ""),
            getattr(o, "phone", ""),
            getattr(o, "product_name", ""),
            getattr(o, "quantity", ""),
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="orders.xlsx"'
    wb.save(response)
    return response

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("created_at", "name", "phone", "product_name", "quantity")
    actions = [export_orders_to_xlsx]  # ✅ 이 줄이 핵심
