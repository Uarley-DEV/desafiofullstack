from django.urls import path
from .views import * 

app_name = 'subscriptions' #comando responsável por  deixar a app mais inteligente 

urlpatterns = [
    path('', index, name='index'),
    path('plan_index', plan_index, name='plan_index'),
    path('plan_add', plan_add, name='plan_add'),
]