from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Q, Sum

from imoveis.forms import ImovelForm, InquilinoForm
from imoveis.models import Imovel, Inquilino, Aluguel


# Página inicial
def index(request):
    return render(request, 'imoveis/index.html')

# Listagem de Imóveis
def list_imoveis(request):
    query = request.GET.get('q')
    imoveis = Imovel.objects.all()
    
    if query:
        imoveis = imoveis.filter(
            Q(endereco__icontains=query) |
            Q(cidade__icontains=query) |
            Q(estado__icontains=query) |
            Q(preco_aluguel__icontains=query)
        )
    
    return render(request, 'imoveis/list_imoveis.html', {'imoveis': imoveis, 'query': query})

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
    
    total_recebido = alugueis.aggregate(Sum('valor'))['valor__sum'] or 0
    alugueis_pendentes = alugueis.filter(data_vencimento__isnull=True)
    
    return render(request, 'imoveis/relatorio_pagamentos.html', {
        'alugueis': alugueis,
        'total_recebido': total_recebido,
        'alugueis_pendentes': alugueis_pendentes
    })