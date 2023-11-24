from django.db import models
from django.conf import settings
from order.models import *
from client.models import *
import secrets

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.PositiveIntegerField(blank=True, null=True)
    ref = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    payment_method = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return "payment" + " " + str(self.amount)

    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            objects_with_similar_ref = Payment.objects.filter(ref=ref)
            if not objects_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self) -> int:
        return self.amount * 100