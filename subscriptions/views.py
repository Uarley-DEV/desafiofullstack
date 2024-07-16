from .models import *
from django.http import JsonResponse
from .models import *
from django.shortcuts import render
from django.db import DatabaseError
from subscriptions.serializador import *
import io
import base64
import qrcode
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404

def index(request):
    return render(request, 'subscriptions/index.html')

def plan_admin(request):
    return render(request, 'subscriptions/plan_admin.html')

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
            'aviso': 'Erro ao adicionar o Plano'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Adicionado com sucesso!'},
            status=200)


def plan_list(request):
    try:
        print('aquiiiii')
        dados= PlanSerializer(Plan.objects.all().order_by('plan_value'), many=True)
        print('dadosss',dados)
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error,
            'aviso': 'Problema ao consultar os dados'},
            status=500)
    else:
        return JsonResponse({'dados':dados.data})
    

def plan_atb(request):
    try:
        item = PlanSerializer(Plan.objects.get(pk=request.GET['plan_id']))
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error, 
            'aviso': 'Problema ao consultar os dados'}, 
            status=500)
    else:
        return JsonResponse(item.data) 
    

def plan_edt(request):
    try:
        plan = Plan.objects.get(pk=request.POST['plan_id'])
        if request.method=="POST":
            plan.plan_id=request.POST['plan_id']
            plan.plan_name=request.POST['plan_name']
            plan.plan_value=request.POST['plan_value']
            plan.plan_storage=request.POST['plan_storage']
            plan.plan_quotas=request.POST['plan_quotas']
            plan.save()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao editar o Plano'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Editado com sucesso!'},
            status=200)


def plan_del(request):
    try:
        if request.method=="POST":
            item=Plan.objects.get(pk=request.POST['plan_id'])
            item.delete()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao deletar o Plano, '},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Excluido com sucesso!'},
            status=200) 
    
def plan_client(request):
    return render(request, 'subscriptions/plan_client.html')


def generate_qr_code(content):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(content)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return img_str

def payment_pix(request, plan_id):
    chave_pix = 'chave_pix_exemplo'
    qr_code_base64 = generate_qr_code(chave_pix)
    plan = Plan.objects.filter(plan_id=plan_id).first()

    if not plan:
        return HttpResponse("Plano não encontrado", status=404)

    context = {
        'qr_code_base64': qr_code_base64,
        'value': plan.plan_value,
        'key_pix': '31996213672',
        'description': plan.plan_name,
        'plan': plan.plan_id
    }

    return render(request, 'subscriptions/payment_frm.html', context)

def payment_add(request):
    user_id = 1

    user_profile = get_object_or_404(UserProfile, pk=user_id)
    contract = Contract()
    contract.plan = Plan.objects.get(pk=request.POST['plan'])  
    contract.user_profile = user_profile 
    contract.status = True
    contract.save()

    #salvar pagamento

    return render(request, 'subscriptions/index.html')  
   
