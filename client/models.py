from django.db import models
from account.models import *

# Create your models here.

class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    task_details = models.TextField()
    contact = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)
