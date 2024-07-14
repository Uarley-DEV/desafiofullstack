from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import *


def index(request):
    return render(request, 'base/base.html')


def entrar(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            request.session.set_expiry(60)
            login(request, user)
            return HttpResponseRedirect(reverse('base:index'))
        else:
            return render(request, 'base/login.html')
        
    else:
        return render(request, 'base/login.html')   
        
        
def sair(request):
    logout(request)
    return HttpResponseRedirect(reverse(':entrar'))        
