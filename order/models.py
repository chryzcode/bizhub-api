from django.db import models
import uuid
from account.models import *
from client.models import *


# Create your models here.

ORDER_TYPE_CHOICES = (
    ("SERVICES", "SERVICES"),
    ("SALES", "SALES")
)


class Order(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES)
    description = models.TextField()
    due_date = models.DateField()
    amount = models.IntegerField(default=0)
    billing_status = models.BooleanField(default=False)
    currency_code = models.CharField(max_length=50, default='NGN')
    currency_symbol = models.CharField(max_length=10, default="₦")
    issue_date = models.DateField(auto_now_add=True)
    class Meta:
        ordering = ("-issue_date",)


    def __str__(self):
        return str(self.id)

