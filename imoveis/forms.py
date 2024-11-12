from django import forms
from imoveis.models import Imovel, Inquilino, Aluguel, ImagemImovel

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ImagemImovelForm(forms.ModelForm):
    class Meta:
        model = ImagemImovel
        fields = ['imagem', 'destaque']
    
class ImovelForm(forms.ModelForm):
    imagens = forms.FileField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}), required=False)
    #imagem = MultipleFileField(label='Selecione as fotos', required=False)
    
    class Meta:
        model = Imovel
        fields = ['tipo_imovel', 'cep', 'endereco', 'bairro', 'cidade', 'estado', 'preco_aluguel', 'descricao']
        widgets = {
            'tipo_imovel': forms.Select(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o CEP'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o endereço'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o bairro'}),
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
    
    def clean_imagens(self):
        imagens = self.files.getlist('imagens')
        if len(imagens) > 5:
            raise forms.ValidationError('Você pode fazer upload de no máximo 5 imagens.')
        return imagens

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