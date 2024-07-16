from django.urls import path
from .views import * 

app_name = 'subscriptions' #comando responsável por  deixar a app mais inteligente 

urlpatterns = [
    path('', index, name='index'),
    path('plan_admin/', plan_admin, name='plan_admin'),
    path('plan_add/', plan_add, name='plan_add'),
    path('plan_list/', plan_list, name='plan_list'),
    path('plan_atb/', plan_atb, name='plan_atb'),
    path('plan_edt/', plan_edt, name='plan_edt'),
    path('plan_del/', plan_del, name='plan_del'),

    path('plan_client/', plan_client, name='plan_client'),
    path('payment_pix/<int:plan_id>/', payment_pix, name='payment_pix'),
    path('payment_add/', payment_add, name='payment_add'),
     
]