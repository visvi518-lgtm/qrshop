from django.shortcuts import render
from .forms import OrderForm

def entry(request):
    return render(request, "entry.html")

def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "order_done.html")
    else:
        form = OrderForm()
    return render(request, "order_form.html", {"form": form})

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Order

@login_required
def export_orders_xlsx(request):
    if not request.user.is_staff:
        return HttpResponse("Forbidden", status=403)

    wb = Workbook()
    ws = wb.active
    ws.title = "Orders"

    ws.append(["created_at", "name", "phone", "address", "product_name", "quantity"])

    for o in Order.objects.order_by("-created_at"):
        ws.append([
            o.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            o.name,
            o.phone,
            o.address,
            o.product_name,
            o.quantity,
        ])

    resp = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    resp["Content-Disposition"] = 'attachment; filename="orders.xlsx"'
    wb.save(resp)
    return resp

from django.http import JsonResponse
from .models import Order

def name_suggestions(request):
    q = request.GET.get("q", "")
    names = (
        Order.objects
        .filter(name__icontains=q)
        .values_list("name", flat=True)
        .distinct()[:10]
    )
    return JsonResponse(list(names), safe=False)

