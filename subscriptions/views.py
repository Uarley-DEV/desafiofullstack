from .models import *
from django.http import JsonResponse
from .models import *
from django.shortcuts import render
from django.db import DatabaseError

def index(request):
    return render(request, 'subscriptions/index.html')

def plan_index(request):
    return render(request, 'subscriptions/plan_index.html')

def plan_add(request):
    try:
        plan = Plan()
        plan.plan_name = request.POST['plan_name']
        plan.plan_value = request.POST['plan_value']
        plan.plan_storage = request.POST['plan_storage']
        plan.plan_quotas = request.POST['plan_quotas']
        plan.save()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao adicionar o Produto'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Adicionado com sucesso!'},
            status=200)