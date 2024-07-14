from django.db import models
from django.contrib.auth.models import User

class Plan(models.Model):
    plan_id = models.BigAutoField(primary_key=True)
    plan_name = models.CharField(max_length=255)
    plan_value = models.FloatField()
    plan_quotas = models.IntegerField()
    plan_storage = models.IntegerField()

    def __str__(self):
        return self.plan_name

class Contract(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} - {self.plan.name}'

class Payment(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.contract.user.username} - {self.amount}'