from django.contrib import admin
from django.urls import path
from shop import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.entry, name="entry"),
    path("order/", views.order_name, name="order_name"),
    path("order/customer/", views.order_customer, name="order_customer"),
    path("order/new/", views.order_new, name="order_new"),
    path("order/done/", views.order_done, name="order_done"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("admin-tools/customers.xlsx", views.export_customers_xlsx, name="export_customers_xlsx"),
    path("admin-tools/customers/import/", views.import_customers_xlsx, name="import_customers_xlsx"),
    path("admin-tools/orders.xlsx", views.export_orders_xlsx, name="export_orders_xlsx"),

]
