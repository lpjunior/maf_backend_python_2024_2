from django.shortcuts import render
from imoveis.models import Imovel, Inquilino

# Página inicial
def index(request):
    return render(request, 'imoveis/index.html')

# Listagem de Imóveis
def list_imoveis(request):
    imoveis = Imovel.objects.all()
    return render(request, 'imoveis/list_imoveis.html', {'imoveis': imoveis})

# Listagem de Inquilinos
def list_inquilinos(request):
    inquilinos = Inquilino.objects.all()
    return render(request, 'imoveis/list_inquilinos.html', {'inquilinos': inquilinos})