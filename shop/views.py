from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Order
from .forms import NameLookupForm, CustomerForm, OrderForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl import load_workbook


def entry(request):
    return render(request, "entry.html", {
        "is_staff": request.user.is_authenticated and request.user.is_staff
    })

def order_start(request):
    matches = []
    query_name = ""

    if request.method == "POST":
        # 신규 고객 생성 폼 제출
        if request.POST.get("create_new") == "1":
            cform = CustomerForm(request.POST)
            if cform.is_valid():
                customer = cform.save()
                request.session["customer_id"] = customer.id
                return redirect("order_new")  # 다음 단계에서 만들 예정
        else:
            cform = CustomerForm()

        # 이름 조회
        lookup = NameLookupForm(request.POST)
        if lookup.is_valid():
            query_name = lookup.cleaned_data["name"].strip()
            matches = Customer.objects.filter(name__icontains=query_name)[:10]

        return render(request, "order_start.html", {
            "lookup": lookup,
            "matches": matches,
            "cform": cform,
            "query_name": query_name,
        })

    return render(request, "order_start.html", {
        "lookup": NameLookupForm(),
        "matches": [],
        "cform": CustomerForm(),
        "query_name": "",
    })
def order_name(request):
    if request.method == "POST":
        form = NameLookupForm(request.POST)
        if form.is_valid():
            request.session["lookup_name"] = form.cleaned_data["name"].strip()
            return redirect("order_customer")
    else:
        form = NameLookupForm()
    return render(request, "order_name.html", {"form": form})

from django.shortcuts import render, redirect, get_object_or_404

def order_customer(request):
    name = request.session.get("lookup_name", "").strip()
    if not name:
        return redirect("order_name")

    matches = Customer.objects.filter(name__icontains=name).order_by("name")[:10]

    # 기존 고객 선택
    if request.method == "POST" and request.POST.get("selected_customer_id"):
        cid = int(request.POST["selected_customer_id"])
        customer = get_object_or_404(Customer, id=cid)
        request.session["customer_id"] = customer.id
        return redirect("order_new")  # 다음 단계에서 만들 주문 화면

    # 신규 고객 생성
    if request.method == "POST" and request.POST.get("create_new") == "1":
        cform = CustomerForm(request.POST)
        if cform.is_valid():
            customer = cform.save()
            request.session["customer_id"] = customer.id
            return redirect("order_new")
    else:
        cform = CustomerForm(initial={"name": name})

    return render(request, "order_customer.html", {
        "name": name,
        "matches": matches,
        "cform": cform,
    })

def order_new(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("order_name")  # 고객 선택부터 다시

    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = customer
            order.save()  # total_price 자동 계산됨
            request.session["last_order_id"] = order.id
            return redirect("order_done")
    else:
        form = OrderForm()

    return render(request, "order_form.html", {"form": form, "customer": customer})

def order_done(request):
    order_id = request.session.get("last_order_id")
    customer_id = request.session.get("customer_id")
    if not order_id or not customer_id:
        return redirect("order_name")

    customer = get_object_or_404(Customer, id=customer_id)
    order = get_object_or_404(Order, id=order_id, customer=customer)
    return render(request, "order_done.html", {"customer": customer, "order": order})

def my_orders(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("order_name")

    customer = get_object_or_404(Customer, id=customer_id)
    orders = Order.objects.filter(customer=customer).order_by("-created_at")

    return render(request, "my_orders.html", {
        "customer": customer,
        "orders": orders,
    })

@login_required
def export_customers_xlsx(request):
    if not request.user.is_staff:
        return HttpResponse("Forbidden", status=403)

    wb = Workbook()
    ws = wb.active
    ws.title = "Customers"
    ws.append(["name", "phone", "address"])

    for c in Customer.objects.order_by("name", "phone"):
        ws.append([c.name, c.phone, c.address])

    resp = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    resp["Content-Disposition"] = 'attachment; filename="customers.xlsx"'
    wb.save(resp)
    return resp

def export_orders_xlsx(request):
    if not request.user.is_staff:
        return HttpResponse("Forbidden", status=403)

    wb = Workbook()
    ws = wb.active
    ws.title = "Orders"

    ws.append(["created_at", "name", "phone", "address", "product", "quantity", "unit_price", "total_price"])

    for o in Order.objects.select_related("customer").order_by("-created_at"):
        ws.append([
            o.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            o.customer.name,
            o.customer.phone,
            o.customer.address,
            o.get_product_display(),
            o.quantity,
            o.unit_price,
            o.total_price,
        ])

    resp = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    resp["Content-Disposition"] = 'attachment; filename="orders.xlsx"'
    wb.save(resp)
    return resp


def import_customers_xlsx(request):
    if not request.user.is_staff:
        return HttpResponse("Forbidden", status=403)

    if request.method == "POST" and request.FILES.get("file"):
        wb = load_workbook(request.FILES["file"])
        ws = wb.active

        # 첫 줄은 헤더라고 가정: name | phone | address
        for row in ws.iter_rows(min_row=2, values_only=True):
            name, phone, address = row
            if not name:
                continue

            Customer.objects.update_or_create(
                name=name.strip(),
                phone=(phone or "").strip(),
                defaults={
                    "address": (address or "").strip(),
                },
            )

        return redirect("/admin/")

    return render(request, "import_customers.html")