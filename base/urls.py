from django.urls import path
from .views import * 

app_name = 'base' #comando responsável por  deixar a app mais inteligente 

urlpatterns = [
    path('', index, name='index'),
    path('entrar/', entrar, name='entrar'),
    path('sair/', sair, name='sair'),
]