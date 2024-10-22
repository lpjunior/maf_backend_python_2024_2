from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('imoveis/', views.list_imoveis, name='list_imoveis'),
    path('inquilinos/', views.list_inquilinos, name='list_inquilinos'),
]
