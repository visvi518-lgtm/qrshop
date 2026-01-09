from django.contrib import admin
from django.urls import path

from orders.views import (
    entry,
    order_create,
    export_orders_xlsx,
    name_suggestions,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", entry, name="entry"),
    path("order/", order_create, name="order_create"),

    path("export/orders.xlsx", export_orders_xlsx, name="export_orders_xlsx"),

    # ✅ 이름 자동완성 API
    path("api/names/", name_suggestions, name="name_suggestions"),
]
