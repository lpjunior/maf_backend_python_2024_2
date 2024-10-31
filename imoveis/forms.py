from django import forms
from imoveis.models import Imovel, Inquilino, Aluguel


class ImovelForm(forms.ModelForm):
    class Meta:
        model = Imovel
        fields = ['endereco', 'cidade', 'estado', 'preco_aluguel', 'descricao']
        widgets = {
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o endereço'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite a cidade'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o estado'}),
            'preco_aluguel': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite o preço do aluguel'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Digite uma descrição do imóvel (opcional)', 'rows': 3, 'maxlength': 150}),            
        }
        
    def clean_preco_aluguel(self):
        preco_aluguel = self.cleaned_data.get('preco_aluguel')
        if preco_aluguel <= 0:
            raise forms.ValidationError("O preço de aluguel deve ser um valor positivo.")
        return preco_aluguel

class InquilinoForm(forms.ModelForm):
    class Meta:
        model = Inquilino
        fields = ['nome', 'telefone', 'email', 'imovel']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o telefone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite o email'}),
            'imovel': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Escolha o imóvel'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("O campo email é obrigatório.")
        return email

class AluguelForm(forms.ModelForm):
    class Meta:
        model = Aluguel
        fields = ['inquilino', 'data_vencimento', 'valor', 'pago']
        widgets = {
            'inquilino': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Escolha o inquilino'}),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite o preço do aluguel'}),
            'pago': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }