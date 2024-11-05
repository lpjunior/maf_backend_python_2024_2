from django.urls import path
from . import views

urlpatterns = [
    # rotas abertas
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('imoveis/', views.list_imoveis, name='list_imoveis'),
    
    # rotas fechadas    
    
    ## Rota de imóveis
    path('imoveis/adicionar/', views.adicionar_imovel, name='adicionar_imovel'),
    path('imoveis/editar/<int:imovel_id>', views.editar_imovel, name='editar_imovel'),
    path('imoveis/excluir/<int:imovel_id>', views.excluir_imovel, name='excluir_imovel'),
    path('imoveis/detalhar_imovel/<int:imovel_id>', views.detalhar_imovel, name='detalhar_imovel'),
    
    # Rota de consulta de CEP
    path('buscar-endereco/', views.buscar_endereco, name='buscar_endereco'),
    
    ## Rota de Relatórios
    path('relatorios/relatorio_pagamentos/', views.relatorio_pagamentos, name='relatorio_pagamentos'),
    path('relatorios/exportar_relatorio_csv/', views.exportar_relatorio_csv, name='exportar_relatorio_csv'),
    path('relatorios/relatorio_avancado_json/', views.relatorio_avancado_json, name='relatorio_avancado_json'),
    
    ## Rota de Inquilinos
    path('inquilinos/', views.list_inquilinos, name='list_inquilinos'),
    path('inquilinos/adicionar/', views.adicionar_inquilino, name='adicionar_inquilino'),
    path('inquilinos/editar/<int:inquilino_id>', views.editar_inquilino, name='editar_inquilino'),
    path('inquilinos/excluir/<int:inquilino_id>', views.excluir_inquilino, name='excluir_inquilino'),

    # Rota de Alugueis
    path('alugueis/', views.listar_alugueis, name='listar_alugueis'),
    path('alugueis/adicionar/', views.cadastrar_aluguel, name='cadastrar_aluguel'),
    path('alugueis/editar/<int:aluguel_id>', views.editar_aluguel, name='editar_aluguel'),
    path('alugueis/marcar_como_pago/<int:aluguel_id>', views.marcar_como_pago, name='marcar_como_pago'),
    path('alugueis/excluir/<int:aluguel_id>', views.excluir_aluguel, name='excluir_aluguel'),
    
    # Rota de E-mails
    path('notificacao/contato_imovel', views.contato_imovel, name='contato_imovel'),
]