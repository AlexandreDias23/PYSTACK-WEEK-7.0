from django.urls import path

from . import views

urlpatterns = [
    path('definir_contas/', views.definir_contas, name="definir_contas"),
    path('ver_contas/', views.ver_contas, name="ver_contas"),
    path('update_conta/<int:id>', views.update_conta, name="update_conta"),
]
