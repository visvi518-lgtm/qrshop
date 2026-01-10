# orders/forms.py
import re
from django import forms
from .models import Order

PRODUCT_CHOICES = [
    ("레드향 5키로", "레드향 5키로"),
    ("레드향 10키로", "레드향 10키로"),
    ("천혜향 5키로", "천혜향 5키로"),
    ("천혜향 10키로", "천혜향 10키로")
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
    
    def clean_phone(self):
        raw = self.cleaned_data.get("phone", "")
        digits = re.sub(r"\D", "", raw)

        # 11자리(010xxxxxxxx) / 10자리(02xxxxxxx 등) 대응
        if len(digits) == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        if len(digits) == 10:
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        raise forms.ValidationError("전화번호 형식이 올바르지 않습니다.")
    
    