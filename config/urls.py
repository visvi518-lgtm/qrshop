from django.contrib import admin
from django.urls import path
from orders import views

urlpatterns = [
    path("export/orders.xlsx", views.export_orders_xlsx, name="export_orders_xlsx"),
    path("admin/", admin.site.urls),
    path("", views.entry, name="entry"),
    path("order/", views.order_create, name="order_create"),
]
