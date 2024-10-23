from django.shortcuts import render, get_object_or_404, redirect
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
def list_inquilinos(request):
    inquilinos = Inquilino.objects.all()
    return render(request, 'imoveis/list_inquilinos.html', {'inquilinos': inquilinos})

# Editar Imóvel
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
def excluir_imovel(request, imovel_id):
    imovel = get_object_or_404(Imovel, id=imovel_id)
    if request.method == 'POST':
        imovel.delete()
        return redirect('list_imoveis')
    return render(request, 'imoveis/excluir_imovel.html', {'imovel': imovel})