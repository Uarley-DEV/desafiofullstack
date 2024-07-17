from .models import *
from django.http import JsonResponse
from .models import *
from django.shortcuts import render
from django.db import DatabaseError
from subscriptions.serializador import *
from datetime import timedelta
import io
import base64
import qrcode
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from datetime import datetime
from dateutil.relativedelta import relativedelta

def index(request):
    return render(request, 'subscriptions/index.html')

    
###############################################################################################################################
#                                          Desciption: Contract                                                               #
###############################################################################################################################
def contract_data(request):
    return render(request, 'subscriptions/contract_list.html')


def contract_list(request):
    try:
        dados = ContractSerializer(Contract.objects.filter(user_profile__user_id=1).order_by('start_date'), many=True)
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),  # Convertendo o erro para string
            'aviso': 'Problema ao consultar os dados'
        }, status=500)
    else:
        return JsonResponse({'dados': dados.data})
    
###############################################################################################################################
#                                          Desciption: Plan                                                                   #
###############################################################################################################################
def plan_admin(request):
    return render(request, 'subscriptions/plan_admin_list.html')


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
    

def plan_data(request):
    return render(request, 'subscriptions/plan_current_list.html')


def plan_list(request):
    try:
        dados= PlanSerializer(Plan.objects.all().order_by('plan_value'), many=True)
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error,
            'aviso': 'Problema ao consultar os dados'},
            status=500)
    else:
        return JsonResponse({'dados':dados.data})


def plan_current_list(request):
    try:
        dados= ContractSerializer(Contract.objects.filter(active=True), many=True)
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
    return render(request, 'subscriptions/plan_client_list.html')

    
###############################################################################################################################
#                                          Desciption: Simulaçao Pix e add de contrat e payment                               #                                 #
###############################################################################################################################
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
    plan = get_object_or_404(Plan, pk=plan_id)
    user_id = 1 
    plan_contract = Contract.objects.filter(user_profile=user_id, active=True).first()
    
    if not plan:
        return HttpResponse("Plano não encontrado", status=404)
    
    credito = 0.0
    saldo_prox_mes = 0.0
    
    if plan_contract:
        # Calcula o crédito disponível do plano anterior, se houver
        data_atual = datetime.now().date()
        data_vencimento = plan_contract.start_date + timedelta(days=30)
        valor_dia = plan_contract.plan.plan_value / 30
        dif = (data_vencimento - data_atual).days
        credito = valor_dia * dif
        
        # Calcula o saldo para o próximo mês
        saldo_prox_mes = credito 
       
        if credito > plan.plan_value:
            context = {
                'qr_code_base64': qr_code_base64,
                'value': 0.0,
                'key_pix': '31996213672',
                'description': plan.plan_name,
                'plan': plan.plan_id,
                'credit': credito,
                'saldo_prox_mes': saldo_prox_mes
            }
        else:
            context = {
                'qr_code_base64': qr_code_base64,
                'value': plan.plan_value - credito,
                'key_pix': '31996213672',
                'description': plan.plan_name,
                'plan': plan.plan_id,
                'credit': credito,
                'saldo_prox_mes': saldo_prox_mes
            }
    else:
        context = {
            'qr_code_base64': qr_code_base64,
            'value': plan.plan_value,
            'key_pix': '31996213672',
            'description': plan.plan_name,
            'plan': plan.plan_id,
            'credit': credito,
            'saldo_prox_mes': saldo_prox_mes
        }

    return render(request, 'subscriptions/payment_frm.html', context)


def payment_add(request):
    try:
        plan_contract = Contract.objects.get(user_profile=1, active=True)

        # Desativa o contrato ativo anterior, se existir
        if plan_contract:
            plan_contract.active = False
            plan_contract.save()

    except Contract.DoesNotExist:
        pass

    user_profile = get_object_or_404(UserProfile, pk=1)

    # Cria um novo contrato com o plano selecionado
    contract = Contract()
    contract.plan = Plan.objects.get(pk=request.POST['plan'])
    contract.user_profile = user_profile
    contract.credits = float(request.POST.get('credit', '0.0').replace(',', '.'))
    contract.active = True
    contract.save()
    
    # Cria um novo pagamento para o contrato
    if request.POST['saldo_prox_mes'] and request.POST['saldo_prox_mes']:
        saldo_prox_mes = float(request.POST['saldo_prox_mes'].replace(',', '.'))
        value = contract.plan.plan_value 
        calc_seq_pg = saldo_prox_mes // value
        calc_rest_pg = saldo_prox_mes % value
        if calc_seq_pg >= 1:
            current_date = datetime.now().date()
            for i in range(int(calc_seq_pg)):
                payment = Payment()
                payment.contract = contract
                payment.amount = float(request.POST.get('value', '0.0').replace(',', '.'))
                payment.active = True
                payment.payment_method = 'Pix'
                payment.user_profile = user_profile
                payment_date = current_date + relativedelta(months=i)
                payment.payment_date = payment_date
                payment.save()
                last_payment_date = payment_date

            if calc_rest_pg > 0:
                payment = Payment()
                payment.contract = contract
                payment.amount = float(contract.plan.plan_value - calc_rest_pg)
                payment.payment_date = last_payment_date + relativedelta(months=1) 
                payment.active = True
                payment.payment_method = 'Pix'
                payment.user_profile = user_profile
                payment.save()
        else:
                payment = Payment()
                payment.contract = contract
                payment.amount = float(request.POST.get('value', '0.0').replace(',', '.'))
                payment.active = True
                payment.payment_method = 'Pix'
                payment.user_profile = user_profile
                payment.payment_date = datetime.now().date()
                payment.save()
                
    return redirect('subscriptions:plan_data')


def user_data(request):
    return render(request, 'subscriptions/user_list.html')


def user_list(request):
    try:
        dados = UserProfileSerializer(UserProfile.objects.filter(user_id=1).order_by('user_name'), many=True)
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Problema ao consultar os dados'
        }, status=500)
    else:
        return JsonResponse({'dados': dados.data})

