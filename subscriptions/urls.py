from django.urls import path
from .views import * 

app_name = 'subscriptions' #comando responsável por  deixar a app mais inteligente 

urlpatterns = [
    path('', index, name='index'),

    #contract
    path('contract_list/', contract_list, name='contract_list'),
    path('contract_data/', contract_data, name='contract_data'),

    #plan
    path('plan_admin/', plan_admin, name='plan_admin'),
    path('plan_client/', plan_client, name='plan_client'),
    path('plan_add/', plan_add, name='plan_add'),
    path('plan_list/', plan_list, name='plan_list'),
    path('plan_current_list/', plan_current_list, name='plan_current_list'),
    path('plan_atb/', plan_atb, name='plan_atb'),
    path('plan_edt/', plan_edt, name='plan_edt'),
    path('plan_data/', plan_data, name='plan_data'),
    path('plan_del/', plan_del, name='plan_del'),

    #payment
    path('payment_pix/<int:plan_id>/', payment_pix, name='payment_pix'),
    path('payment_add/', payment_add, name='payment_add'),

    #user
    path('user_list/', user_list, name='user_list'),
    path('user_data/', user_data, name='user_data'),
     
]