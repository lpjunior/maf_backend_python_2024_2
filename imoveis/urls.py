from django.urls import path
from . import views

urlpatterns = [
    # rotas abertas
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('imoveis/', views.list_imoveis, name='list_imoveis'),
    
    # rotas fechadas    
    path('imoveis/adicionar/', views.adicionar_imovel, name='adicionar_imovel'),
    path('imoveis/editar/<int:imovel_id>', views.editar_imovel, name='editar_imovel'),
    path('imoveis/excluir/<int:imovel_id>', views.excluir_imovel, name='excluir_imovel'),
    
    path('relatorios/relatorio_pagamentos/', views.relatorio_pagamentos, name='relatorio_pagamentos'),
    
    path('inquilinos/', views.list_inquilinos, name='list_inquilinos'),
    path('inquilinos/adicionar/', views.adicionar_inquilino, name='adicionar_inquilino'),
    path('inquilinos/editar/<int:inquilino_id>', views.editar_inquilino, name='editar_inquilino'),
]