from django.contrib import admin
from django.urls import path
from .views import pagina_inicial, login_usuario, cadastrar_usuario, adicionar_imovel, detalhes_imovel, editar_imovel, \
    excluir_imovel, logout_usuario

urlpatterns = [
    path('', login_usuario, name='login'),
    path('/pagina_inicial/', pagina_inicial, name='pagina_inicial'),
    path('/cadastro/', cadastrar_usuario, name='cadastro'),
    path('/adicionar_imovel/', adicionar_imovel, name='adicionar_imovel'),
    path('/detalhes_imovel/<int:id>/', detalhes_imovel, name='detalhes_imovel'),
    path('/editar_imovel/<int:id>/', editar_imovel, name='editar_imovel'),
    path('excluir_imovel/<int:id>/', excluir_imovel, name='excluir_imovel'),
    path('/logout/', logout_usuario, name='logout')


]
