from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    acc_no = models.CharField(max_length=20, unique=True)
    balance = models.FloatField(default=0)

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)  # Deposit / Withdraw
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
