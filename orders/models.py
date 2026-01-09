from django.db import models

class Order(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=30)
    address = models.TextField()
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.product_name} x{self.quantity}"
