from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('/subscriptions/plan_client')),
    path('subscriptions/', include('subscriptions.urls')),
]
