import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from perfil.models import Categoria
from perfil.utils import calcula_total


def definir_planejamento(request):
    categorias = Categoria.objects.all()
    return render(request, 'definir_planejamento.html', {'categorias': categorias})


@csrf_exempt
def update_valor_categoria(request, id):
    novo_valor = json.load(request)['novo_valor']
    categoria = Categoria.objects.get(id=id)
    categoria.valor_planejamento = novo_valor
    categoria.save()

    return JsonResponse({'status': 'Sucesso'})


def ver_planejamento(request):
    categorias = Categoria.objects.all()
    total_planejamento = calcula_total(categorias, 'valor_planejamento')
    valor_total_gasto = sum(categoria.total_gasto() for categoria in categorias)
    percentual = int((valor_total_gasto * 100) / total_planejamento)
    return render(request, 'ver_planejamento.html', {'categorias': categorias, 'total_planejamento': total_planejamento, 'valor_total_gasto': valor_total_gasto, 'percentual': percentual})
