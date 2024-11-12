import csv
import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags

from gestao_alugueis.utils import enviar_email
from imoveis.forms import ImovelForm, InquilinoForm, AluguelForm
from imoveis.models import Imovel, Inquilino, Aluguel, ImagemImovel
from imoveis.services.geocode import get_coordinates_from_address
from imoveis.services.search_address_by_cep import buscar_endereco_por_cep

# Página inicial
def index(request):
    return render(request, 'index.html')

# Adicionar Inquilino
@login_required
def adicionar_inquilino(request):
    if request.method == 'POST':
        form = InquilinoForm(request.POST, request.FILES)
        if form.is_valid():
            imovel = form.save()
            
            for imagem in request.FILES.getlist('imagens'):
                ImagemImovel.objects.create(imovel=imovel, imagem=imagem)
            
            return redirect('list_inquilinos')
    else:
        form = InquilinoForm()
    return render(request, 'inquilinos/form_inquilino.html', {'form': form, 'title': 'Adicionar Inquilino'})

# Editar Inquilino
@login_required
def editar_inquilino(request, inquilino_id):
    inquilino = get_object_or_404(Inquilino, id=inquilino_id)
    if request.method == 'POST':
        form = InquilinoForm(request.POST)
        form.save()
        
        return redirect('list_inquilinos')
    else:
        form = InquilinoForm(instance=inquilino)
    return render(request, 'inquilinos/form_inquilino.html', {'form': form, 'title': 'Editar Inquilino'})


# Listagem de Inquilinos
@login_required
def list_inquilinos(request):
    inquilinos = Inquilino.objects.all()
    return render(request, 'inquilinos/list_inquilinos.html', {'inquilinos': inquilinos})

# Excluir Inquilino
@login_required
def excluir_inquilino(request, inquilino_id):
    inquilino = get_object_or_404(Inquilino, id=inquilino_id)
    if request.method == 'POST':
        inquilino.delete()
        return redirect('list_inquilinos')
    return render(request, 'inquilinos/excluir_inquilino.html', {'inquilino': inquilino})

# Buscar CEP
@login_required
def buscar_endereco(request):
    cep = request.GET.get('cep')
    if not cep:
        return JsonResponse({'erro': 'CEP não fornecido.'}, status=400)
    
    try:
        dados = buscar_endereco_por_cep(cep)
        return JsonResponse({
            'endereco': dados['logradouro'],
            'bairro': dados['bairro'],
            'cidade': dados['localidade'],
            'estado': dados['uf'],
            'cep': dados['cep'],
        })
    except Exception as e:
        return JsonResponse({'erro': f'Erro: {str(e)}'}, status=500)

def detalhar_imovel(request, imovel_id):
    imovel = get_object_or_404(Imovel, id=imovel_id)
    imagens = imovel.imagens.all()
    
    print(imagens)

    latitude,longitude,display_name = get_coordinates_from_address(cep=imovel.cep)

    return render(request, 'imoveis/detalhar_imovel.html', {
        'imovel': imovel,
        'imagens': imagens,
        'latitude': latitude,
        'longitude': longitude,
        'display_name': display_name
    })

# Vitrine de Imóveis
def vitrine_imoveis(request):
    # Filtra os imóveis que não possuem inquilinos (imóveis disponíveis)
    imoveis_disponiveis = Imovel.objects.filter(~Q(id__in=Inquilino.objects.values('imovel_id')))

    # Para cada imóvel disponível, tenta pegar a imagem destacada ou a primeira imagem disponível
    for imovel in imoveis_disponiveis:
        # Busca a imagem destacada ou, caso não tenha, pega a primeira imagem
        imagem_destaque = imovel.imagens.filter(destaque=True).first() or imovel.imagens.first()
        imovel.imagem_destaque = imagem_destaque  # Adiciona dinamicamente o atributo para facilitar o uso no template

    return render(request, 'imoveis/vitrine.html', {'imoveis': imoveis_disponiveis})

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

# Adicionar Imóvel
@login_required
def adicionar_imovel(request):
    if request.method == 'POST':
        form = ImovelForm(request.POST, request.FILES)
        if form.is_valid():
            imovel = form.save()

            print(f'============> {request.FILES}')
            for imagem in request.FILES.getlist('imagens'):
                print(f'============> {imagem}')
                ImagemImovel.objects.create(imovel=imovel, imagem=imagem)
            
            return redirect('list_imoveis')
    else:
        form = ImovelForm()
    return render(request, 'imoveis/form_imovel.html', {'form': form, 'title': 'Adicionar Imóvel'})

# Editar Imóvel
@login_required
def editar_imovel(request, imovel_id):
    imovel = get_object_or_404(Imovel, id=imovel_id)
    if request.method == 'POST':
        form = ImovelForm(request.POST, request.FILES, instance=imovel)
        imovel = form.save()

        print(f'============> {request.FILES}')
        for imagem in request.FILES.getlist('imagens'):
            print(f'============> {imagem}')
            ImagemImovel.objects.create(imovel=imovel, imagem=imagem)
            
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
            return render(request, 'login.html', {'error': 'Credenciais inválidas.'})
    return render(request, 'login.html')
    
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
    
    return render(request, 'relatorios/relatorio_pagamentos.html', {
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
def marcar_como_pago(request, aluguel_id):
    aluguel = get_object_or_404(Aluguel, id = aluguel_id)

    if not aluguel.pago:
        aluguel.pago = True
        
        # Solução para somar 30 dias corridos
        aluguel.data_vencimento += timezone.timedelta(days=30)
        
        # Solução para dia fixo de pagamento
        #data_vencimento = aluguel.data_vencimento
        #if data_vencimento.month == 12: # Se for dezembro, o próximo mês é janeiro do próximo ano
        #    nova_data_vencimento = data_vencimento.replace(year=data_vencimento.year + 1, month=1)
        #else:
        #    nova_data_vencimento = data_vencimento.replace(month=data_vencimento.month + 1)

        #aluguel.data_vencimento = nova_data_vencimento
        
        aluguel.save()

        email = aluguel.inquilino.email
        assunto = 'Confirmação de pagamento recebido'
        mensagem_html = render_to_string('email/contato_imovel.html', {
            'titulo_email': 'Contato Sobre Imóvel',
            'content': f'<p>Olá, {aluguel.inquilino.nome}, confirmamos o recebimento do pagamento de R$ {aluguel.valor} referente ao aluguel do imóvel.</p>'
        })

        envia_email(email, assunto, mensagem_html)
        
        messages.success(request, "Pagamento registrado com sucesso.")

    return redirect('listar_alugueis')

def contato_imovel(request):
    try:
        if request.method == 'POST':
            nome = request.POST.get('nome')
            email = request.POST.get('email')
            telefone = request.POST.get('telefone')
            mensagem = request.POST.get('mensagem')
            identificador = request.POST.get('identificador')
            assunto = f'Interesse sobre no Imóvel - {identificador}'
            ano_atual = datetime.datetime.now().year
            
            mensagem_html = render_to_string('email/contato_imovel.html', {
                'titulo_email': 'Contato Sobre Imóvel',
                'content': 
                    f'''<p>Olá, o {nome} está interessado no imóvel {identificador}</p>
                        <p><strong>Telefone:</strong> {telefone}</p>
                        <p><strong>E-mail:</strong> {email}</p>
                        <br>
                        <p><strong>Mensagem do contato:</strong> {mensagem}</p>''',
                'ano_atual': ano_atual
            })
            
            envia_email(email, assunto, mensagem_html)
            
            return redirect('detalhar_imovel', imovel_id=request.POST.get('imovel_id'))
    except Exception as e:
        print(f"Ocorreu um erro ao tentar enviar o email. Erro: {e}")
        
def envia_email(email, assunto, mensagem_html):
    plain_message = strip_tags(mensagem_html)
    enviar_email(
        destinatario=email,
        assunto=assunto,
        mensagem=plain_message,
        mensagem_html=mensagem_html
    )