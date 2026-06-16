from django.db import models
from django.contrib.auth.models import User


# Modelo Cliente
class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil_cliente")
    telefone = models.CharField(max_length=20, verbose_name='Telefone do Cliente')

    def __str__(self):
        return f"Cliente: {self.usuario.username}"


# Modelo Corretor
class Corretor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil_corretor")
    telefone = models.CharField(max_length=20, verbose_name='WhatsApp/Telefone do Corretor')

    def __str__(self):
        return f"Corretor: {self.usuario.username}"


#Modelo do imóvel
class Imovel(models.Model):
    corretor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Corretor Responsável")

    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    tipo_Imovel = models.CharField(max_length=50)
    ano_construcao = models.IntegerField()
    preco = models.FloatField()

    logradouro = models.CharField(max_length=100, verbose_name="Rua/Avenida")
    numero = models.CharField(max_length=10, verbose_name="Número")
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")

    imagem_principal = models.ImageField(upload_to="media/img")

    def __str__(self):
        return f"{self.titulo} ({self.tipo_Imovel})"


#Modelo para receber imagens adicionais do imóvel
class ImagemImovel(models.Model):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE, related_name="imagens")
    imagem = models.ImageField(upload_to="media/img")

    def __str__(self):
        return f"Foto de: {self.imovel.titulo}"
