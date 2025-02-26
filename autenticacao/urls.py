from django.urls import path
from .views import cadastro, login

urlpatterns = [
    path('cadastro/', cadastro),
    path('login/', login),
]
