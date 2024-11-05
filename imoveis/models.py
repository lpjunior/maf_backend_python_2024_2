from django.db import models
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
    cep = models.CharField(max_length=10, default="01001-001")
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=100, default='')
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
        return f"{self.identificador}{self.endereco} - {self.cidade}/{self.estado}"

# Modelo para Inquilinos
class Inquilino(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nome} - {self.imovel.endereco}"

# Modelo para Aluguéis
class Aluguel(models.Model):
    inquilino = models.ForeignKey(Inquilino, on_delete=models.CASCADE)
    data_vencimento = models.DateField()
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    pago = models.BooleanField(default=False)

    def __str__(self):
        return f"Aluguel de {self.inquilino.nome} - {self.data_vencimento}"