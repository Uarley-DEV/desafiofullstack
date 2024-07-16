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


class UserProfile(models.Model): 
    user_id = models.BigAutoField(primary_key=True)
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField(unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user_name
    
class Contract(models.Model):
    contract_id = models.BigAutoField(primary_key=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    status = models.BooleanField()
    credits = models.FloatField(default=0.0)