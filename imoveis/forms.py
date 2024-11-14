import datetime
from django import forms
from decimal import Decimal
from django.db.models import Q
from imoveis.models import Imovel, Inquilino, Aluguel, ImagemImovel

class ImagemImovelForm(forms.ModelForm):
    class Meta:
        model = ImagemImovel
        fields = ['imagem', 'destaque']
    
class ImovelForm(forms.ModelForm):
    imagens = forms.FileField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}), required=False)
    
    class Meta:
        model = Imovel
        fields = ['tipo_imovel', 'cep', 'endereco', 'bairro', 'cidade', 'estado', 'preco_aluguel', 'descricao']
        labels = {
            'tipo_imovel': 'Tipo de Imóvel',
            'cep': 'CEP',
            'endereco': 'Endereço',
            'bairro': 'Bairro',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'preco_aluguel': 'Preço do Aluguel',
            'descricao': 'Descrição do Imóvel',
        }
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
        fields = ['nome', 'telefone', 'email']
        labels = {
            'nome': 'Nome',
            'telefone': 'Telefone',
            'email': 'Email'   
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o telefone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite o email'}),
        }
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("O campo email é obrigatório.")
        return email

class AluguelForm(forms.ModelForm):    
    class Meta:
        model = Aluguel
        fields = ['inquilino', 'imovel', 'data_vencimento', 'valor', 'iptu', 'taxa_incendio', 'condominio', 'outras_taxas', 'pago']
        labels = {
            'inquilino': 'Inquilino',
            'imovel': 'Imóvel',
            'data_vencimento': 'Data de Vencimento',
            'valor': 'Valor',
            'pago': 'Pago',
            'iptu': 'IPTU',
            'taxa_incendio': 'Taxa Incêndio',
            'condominio': 'Condomínio',
            'outras_taxas': 'Outras Taxas',
        }
        widgets = {
            'inquilino': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Escolha o inquilino'}),
            'imovel': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Escolha o imóvel'}),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite o preço do aluguel', 'readonly': 'readonly'}),
            'iptu': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite o preço do IPTU'}),
            'taxa_incendio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite o preço da taxa de incêndio'}),
            'condominio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite o preço do condomínio'}),
            'outras_taxas': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite o somatório de taxas extras'}),
            'pago': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra imóveis
        # No caso de edição, inclui o imóvel já alugado
        if self.instance and self.instance.pk:
            # Adiciona o imóvel do aluguel atual à queryset para que ele apareça na lista
            self.fields['imovel'].queryset = Imovel.objects.filter(
                Q(id=self.instance.imovel.id) | ~Q(id__in=Aluguel.objects.values('imovel_id'))
            )
        else:
            # Em caso de criação, mostra apenas imóveis não alugados
            self.fields['imovel'].queryset = Imovel.objects.exclude(id__in=Aluguel.objects.values('imovel_id'))


        # Formata a data de vencimento no formato YYYY-MM-DD se houver uma data inicial
        if self.instance and self.instance.data_vencimento:
            self.initial['data_vencimento'] = self.instance.data_vencimento.strftime('%Y-%m-%d')

    def clean(self):
        cleaned_data = super().clean()
        
        imovel = cleaned_data.get('imovel')
        if imovel:
            valor_aluguel = imovel.preco_aluguel
        else:
            valor_aluguel = Decimal(0.0)
        
        iptu = cleaned_data.get('iptu') or Decimal(0.0)
        taxa_incendio = cleaned_data.get('taxa_incendio') or Decimal(0.0)
        condominio = cleaned_data.get('condominio') or Decimal(0.0)
        outras_taxas = cleaned_data.get('outras_taxas') or Decimal(0.0)

        valor_final = valor_aluguel + iptu + taxa_incendio + condominio + outras_taxas
        cleaned_data['valor'] = valor_final
        
        return cleaned_data
        
    def clean_data_vencimento(self):
        data_vencimento = self.cleaned_data.get('data_vencimento')
        if data_vencimento < datetime.date.today():
            raise forms.ValidationError("A data de vencimento não pode ser no passado.")
        return data_vencimento