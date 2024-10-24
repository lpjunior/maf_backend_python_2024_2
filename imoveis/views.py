from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from imoveis.forms import ImovelForm
from imoveis.models import Imovel, Inquilino

# Página inicial
def index(request):
    return render(request, 'imoveis/index.html')

# Listagem de Imóveis
def list_imoveis(request):
    imoveis = Imovel.objects.all()
    return render(request, 'imoveis/list_imoveis.html', {'imoveis': imoveis})

# Listagem de Inquilinos
@login_required
def list_inquilinos(request):
    inquilinos = Inquilino.objects.all()
    return render(request, 'imoveis/list_inquilinos.html', {'inquilinos': inquilinos})

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
    return render(request, 'imoveis/editar_imovel.html', {'form': form})

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