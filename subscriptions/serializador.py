from rest_framework import serializers
from.models import*

class ContractSerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source="plan.plan_name", read_only="True")
    plan_value = serializers.FloatField(source="plan.plan_value", read_only="True")
    plan_storage = serializers.CharField(source="plan.plan_storage", read_only="True")
    payment_date = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = '__all__'

    def get_payment_date(self, obj):
        payments = Payment.objects.filter(contract=obj)
        payment_dates = [payment.payment_date.strftime('%d/%m/%Y') for payment in payments]
        
        return ', '.join(payment_dates)


class PlanSerializer(serializers.ModelSerializer):
     plan_active = serializers.SerializerMethodField()

     class Meta:
            model = Plan
            fields = '__all__'

     def get_plan_active(self, obj):
            # Verifica se existe contrato ativo para o plano atual
            contract = Contract.objects.filter(plan=obj, active=True).first()
            if contract and contract.plan:
                return contract.plan.plan_id  # Retorna apenas o ID do plano ativo
            return None  
     
     
class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = '__all__'
