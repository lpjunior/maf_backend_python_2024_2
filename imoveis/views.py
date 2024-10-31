import csv
import datetime
from django.utils import timezone

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Sum

from imoveis.forms import ImovelForm, InquilinoForm, AluguelForm
from imoveis.models import Imovel, Inquilino, Aluguel


# Página inicial
def index(request):
    return render(request, 'imoveis/index.html')

# Listagem de Imóveis
def list_imoveis(request):
    query = Imovel.objects.all()
    cidade = request.GET.get('cidade')
    estado = request.GET.get('estado')
    preco_min = request.GET.get('preco_min')
    preco_max = request.GET.get('preco_max')
    
    if cidade:
        query = query.filter(cidade__icontains=cidade)
    if estado:
        query = query.filter(estado__icontains=estado)
 
    if preco_min and preco_max:
        query = query.filter(preco_aluguel__gte=preco_min, preco_aluguel__lte=preco_max)
    elif preco_min:
        query = query.filter(preco_aluguel__lte=preco_min) # Less Than or Equal (Menor ou igual)
    elif preco_max:
        query = query.filter(preco_aluguel__gte=preco_max) # Greater Than or Equal (Maior ou igual)

    return render(request, 'imoveis/list_imoveis.html', {'imoveis': query})

# Adicionar Inquilino
@login_required
def adicionar_inquilino(request):
    if request.method == 'POST':
        form = InquilinoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_inquilinos')
    else:
        form = InquilinoForm()
    return render(request, 'imoveis/form_inquilino.html', {'form': form, 'title': 'Adicionar Inquilino'})

# Editar Inquilino
@login_required
def editar_inquilino(request, inquilino_id):
    inquilino = get_object_or_404(Inquilino, id=inquilino_id)
    if request.method == 'POST':
        form = InquilinoForm(request.POST, instance=inquilino)
        form.save()
        return redirect('list_inquilinos')
    else:
        form = InquilinoForm(instance=inquilino)
    return render(request, 'imoveis/form_inquilino.html', {'form': form, 'title': 'Editar Inquilino'})


# Listagem de Inquilinos
@login_required
def list_inquilinos(request):
    inquilinos = Inquilino.objects.all()
    return render(request, 'imoveis/list_inquilinos.html', {'inquilinos': inquilinos})

# Adicionar Imóvel
@login_required
def adicionar_imovel(request):
    if request.method == 'POST':
        form = ImovelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_imoveis')
    else:
        form = ImovelForm()
    return render(request, 'imoveis/form_imovel.html', {'form': form, 'title': 'Adicionar Imóvel'})

# Editar Imóvel
@login_required
def editar_imovel(request, imovel_id):
    imovel = get_object_or_404(Imovel, id=imovel_id)
    if request.method == 'POST':
        form = ImovelForm(request.POST, instance=imovel)
        form.save()
        return redirect('list_imoveis')
    else:
        form = ImovelForm(instance=imovel)
    return render(request, 'imoveis/form_imovel.html', {'form': form, 'title': 'Editar Imóvel'})

# Excluir Imóvel
@login_required
def excluir_imovel(request, imovel_id):
    imovel = get_object_or_404(Imovel, id=imovel_id)
    if request.method == 'POST':
        imovel.delete()
        return redirect('list_imoveis')
    return render(request, 'imoveis/excluir_imovel.html', {'imovel': imovel})

# Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')  
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'imoveis/login.html', {'error': 'Credenciais inválidas.'})
    return render(request, 'imoveis/login.html')
    
#Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def relatorio_pagamentos(request):
    alugueis = Aluguel.objects.all()
    total_recebido = alugueis.filter(pago=True).aggregate(Sum('valor'))['valor__sum'] or 0
    alugueis_pendentes = alugueis.filter(pago=False)
    
    # Notificações de vencimento próximos
    hoje = datetime.date.today()
    vencimento_proximo = hoje + datetime.timedelta(days=7)
    alugueis_a_vencer = alugueis.filter(pago=False, data_vencimento__gt=hoje, data_vencimento__lte=vencimento_proximo)
    alugueis_vencidos = alugueis.filter(pago=False, data_vencimento__lt=hoje)
    
    if alugueis_a_vencer.exists(): 
        messages.info(request, f"{alugueis_a_vencer.count()} pagamento(s) esta(ão) próximo(s) do vencimento.")

    if alugueis_vencidos.exists():
        messages.error(request, f"{alugueis_vencidos.count()} pagamento(s) que esta(ão) vencimento(s).")
    
    return render(request, 'imoveis/relatorio_pagamentos.html', {
        'alugueis': alugueis,
        'total_recebido': total_recebido,
        'alugueis_pendentes': alugueis_pendentes,
        'alugueis_a_vencer': alugueis_a_vencer,
        'alugueis_vencidos': alugueis_vencidos
    })

@login_required
def exportar_relatorio_csv(request):
    # Cria a responsa do tipo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio_pagamentos.csv"'
    response.write('\ufeff') # BOM(Byte Order Mark) do UTF-8
    
    # Escreve o cabeçalho e os dados no CSV
    writer = csv.writer(response)
    writer.writerow(['Imóvel', 'Inquilino', 'Data de Vencimento', 'Valor', 'Pago'])
    
    # Obtém os dados do aluguel
    alugueis = Aluguel.objects.all()
    
    for aluguel in alugueis:
        writer.writerow([
            aluguel.inquilino.imovel.endereco,
            aluguel.inquilino.nome,
            aluguel.data_vencimento,
            f"{aluguel.valor:.0f}",
            'Sim' if aluguel.pago else 'Não'
        ])
    
    return response

@login_required
def relatorio_avancado_json(request):
    """
    View para fornecer dados em JSON para relatórios avançados com gráficos.
    """
    alugueis = Aluguel.objects.filter(pago=True).values('data_vencimento').annotate(total=Sum('valor'))
    return JsonResponse(list(alugueis), safe=False)

@login_required
def listar_alugueis(request):
    alugueis = Aluguel.objects.all()
    return render(request, 'alugueis/listar_alugueis.html', {'alugueis' : alugueis})

@login_required
def cadastrar_aluguel(request):
    if request.method == 'POST':
        form = AluguelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_alugueis')
    else:
        form = AluguelForm()
    return render(request, 'alugueis/form_aluguel.html', {'form': form, 'title': 'Cadastrar Aluguel'})

@login_required
def editar_aluguel(request, aluguel_id):
    aluguel = get_object_or_404(Aluguel, id = aluguel_id)
    
    if request.method == 'POST':
        form = AluguelForm(request.POST, instance=aluguel)
        if form.is_valid():
            form.save()
            return redirect('listar_alugueis')
    else:
        form = AluguelForm(instance=aluguel)
    return render(request, 'alugueis/form_aluguel.html', {'form': form, 'aluguel': aluguel, 'title': 'Editar Aluguel'})

@login_required
def excluir_aluguel(request, aluguel_id):
    aluguel = get_object_or_404(Aluguel, id = aluguel_id)

    if request.method == 'POST':
        aluguel.delete()
        return redirect('listar_alugueis')
    
    return render(request, 'alugueis/excluir_aluguel.html', {'aluguel': aluguel})

@login_required
def marcar_como_aluguel(request, aluguel_id):
    aluguel = get_object_or_404(Aluguel, id = aluguel_id)

    if not aluguel.pago:
        aluguel.pago = True
        aluguel.data_vencimento += timezone.timedelta(days=30)
        aluguel.save()
        messages.success(request, "Pagamento registrado com sucesso.")

    return redirect('listar_alugueis')