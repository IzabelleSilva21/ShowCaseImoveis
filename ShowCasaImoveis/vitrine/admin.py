from django.contrib import admin
from .models import Cliente, Corretor, Imovel, ImagemImovel

admin.register(Cliente)
admin.register(Corretor)
admin.register(Imovel)
admin.register(ImagemImovel)
