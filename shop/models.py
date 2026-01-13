from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    phone = models.CharField(max_length=30)
    address = models.TextField()

    def __str__(self):
        return f"{self.name} / {self.phone}"


class Order(models.Model):
    PRODUCT_5 = "REDHYANG_5"
    PRODUCT_10 = "REDHYANG_10"

    PRODUCT_CHOICES = [
        (PRODUCT_5, "레드향 5키로"),
        (PRODUCT_10, "레드향 10키로"),
    ]

    PRICE_MAP = {
        PRODUCT_5: 35000,
        PRODUCT_10: 60000,
    }

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    product = models.CharField(max_length=20, choices=PRODUCT_CHOICES)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.PositiveIntegerField(default=0)
    total_price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.unit_price = self.PRICE_MAP.get(self.product, 0)
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.name} - {self.get_product_display()} x{self.quantity}"
