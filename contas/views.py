import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from perfil.models import Categoria
from .models import ContaPagar, ContaPaga
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt


def definir_contas(request):
    if request.method == "GET":
        categorias = Categoria.objects.all()
        return render(request, 'definir_contas.html', {'categorias': categorias})
    else:
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        dia_pagamento = request.POST.get('dia_pagamento')

        conta = ContaPagar(
            titulo=titulo,
            categoria_id=categoria,
            descricao=descricao,
            valor=valor,
            dia_pagamento=dia_pagamento
        )

        conta.save()

        messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso')
        return redirect('/contas/definir_contas')


def ver_contas(request):
    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day

    contas = ContaPagar.objects.all()
    contas_pagas = ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).values('conta')
    contas_vencidas = contas.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_pagas)
    contas_proximas_vencimento = contas.filter(dia_pagamento__lte=DIA_ATUAL + 5).filter(dia_pagamento__gte=DIA_ATUAL).exclude(id__in=contas_pagas)
    restantes = contas.exclude(id__in=contas_vencidas).exclude(id__in=contas_pagas).exclude(id__in=contas_proximas_vencimento)

    total_pagas = contas_pagas.aggregate(total=Count('id'))['total']
    total_vencidas = contas_vencidas.aggregate(total=Count('id'))['total']
    total_proximas_vencimento = contas_proximas_vencimento.aggregate(total=Count('id'))['total']
    total_restantes = restantes.aggregate(total=Count('id'))['total']

    return render(request, 'ver_contas.html', {'contas_vencidas': contas_vencidas, 'contas_proximas_vencimento': contas_proximas_vencimento, 'restantes': restantes,
                                               'total_pagas': total_pagas, 'total_vencidas': total_vencidas, 'total_proximas_vencimento': total_proximas_vencimento, 'total_restantes': total_restantes})


@csrf_exempt
def update_conta(request, id):
    print(id)
    conta = ContaPaga(
        data_pagamento=datetime.now(),
        conta_id=id
    )
    conta.save()
    return JsonResponse({'status': 'Sucesso'})
