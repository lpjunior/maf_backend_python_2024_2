from django.db import models
from decimal import Decimal
import random

TIPO_IMOVEL_CHOICES = [
    ('CAS', 'Casa'),
    ('APT', 'Apartamento'),
    ('LOJ', 'Loja'),
    ('SAL', 'Sala'),
    ('TER', 'Terreno')
]

# Modelo para Imóveis
class Imovel(models.Model):
    tipo_imovel = models.CharField(max_length=3, choices=TIPO_IMOVEL_CHOICES, default="CAS")
    identificador = models.CharField(max_length=10, unique=True) 
    cep = models.CharField(max_length=10)
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    preco_aluguel = models.DecimalField(max_digits=8, decimal_places=2)
    descricao = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.identificador:
            while True:
                prefixo = self.tipo_imovel
                sufixo = str(random.randint(10000, 99999))
                identificador = f"{prefixo}-{sufixo}"
                if not Imovel.objects.filter(identificador=identificador).exists():
                    self.identificador = identificador
                    break;
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.identificador}"

# Modelo para as imagens do imovel
class ImagemImovel(models.Model):
    imovel = models.ForeignKey(Imovel, related_name='imagens', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='imoveis/')
    destaque = models.BooleanField(default=False)
    data_upload = models.DateTimeField(auto_now_add=True)

# Modelo para Inquilinos
class Inquilino(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    
    def __str__(self):
        return f"{self.nome} - {self.email}"

# Modelo para Aluguéis
class Aluguel(models.Model):
    inquilino = models.ForeignKey(Inquilino, on_delete=models.CASCADE)
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    data_vencimento = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    pago = models.BooleanField(default=False)
    iptu = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.0'), blank=True, null=True)
    taxa_incendio = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.0'), blank=True, null=True)
    condominio = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.0'), blank=True, null=True)
    outras_taxas = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.0'), blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calcula o valor total considerando o preço do aluguel e as taxas
        preco_aluguel = self.imovel.preco_aluguel if self.imovel else Decimal('0.0')
        self.valor = preco_aluguel + (self.iptu or Decimal('0.0')) + (self.taxa_incendio or Decimal('0.0')) + \
                     (self.condominio or Decimal('0.0')) + (self.outras_taxas or Decimal('0.0'))
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Aluguel de {self.inquilino.nome} - {self.data_vencimento} - R$ {self.valor}"