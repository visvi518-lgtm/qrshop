# forms.py
from django import forms
from .models import Order

PRODUCT_CHOICES = [
    ("아메리카노", "아메리카노"),
    ("카페라떼", "카페라떼"),
    ("카푸치노", "카푸치노"),
]

class OrderForm(forms.ModelForm):
    product_name = forms.ChoiceField(
        choices=PRODUCT_CHOICES,
        label="상품명"
    )

    class Meta:
        model = Order
        fields = ["name", "phone", "address", "product_name", "quantity"]
        labels = {
            "name": "이름",
            "phone": "전화번호",
            "address": "주소",
            "quantity": "수량",
        }
