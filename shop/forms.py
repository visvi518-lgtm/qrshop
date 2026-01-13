import re
from django import forms
from .models import Customer
from .models import Order

class NameLookupForm(forms.Form):
    name = forms.CharField(label="이름", max_length=50)

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "phone", "address"]
        labels = {"name": "이름", "phone": "전화번호", "address": "주소"}

    def clean_phone(self):
        raw = self.cleaned_data.get("phone", "")
        digits = re.sub(r"\D", "", raw)
        if len(digits) == 11:
            return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
        if len(digits) == 10:
            return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        raise forms.ValidationError("전화번호 형식이 올바르지 않습니다.")
    
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["product", "quantity"]
        labels = {"product": "제품", "quantity": "수량"}

