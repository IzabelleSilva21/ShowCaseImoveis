from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.decorators.http import require_POST

from .forms import ImovelForm, ClienteForm, CorretorForm, EditarUsuarioForm, CadastroUsuarioForm
from .models import *

#decorador que verifica se o usuario está logado e se é um corretor
def corretor_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Você precisa estar logado para acessar esta página!')
            return redirect('login')
        if not hasattr(request.user, 'perfil_corretor'):
            messages.error(request, 'Apenas usuários do tipo Corretor podem realizar essa ação!')
            return redirect('pagina_inicial')
        return view_func(request, *args, **kwargs)
    return wrapped_view


def pagina_inicial(request):
    lista_imoveis = Imovel.objects.all()
    return render(request, 'pagina_inicial.html', {'imoveis': lista_imoveis})


@corretor_required
def adicionar_imovel(request):

    if request.method == "POST":
        form = ImovelForm(request.POST, request.FILES)
        if form.is_valid():
            novo_imovel = form.save(commit=False)
            novo_imovel.corretor = request.user
            novo_imovel.save()

            #Captura a lista de imagens adicionais
            imagens_adicionais = request.FILES.getlist('imagens_adicionais')
            for foto in imagens_adicionais:
                ImagemImovel.objects.create(imovel=novo_imovel, imagem=foto)

            messages.success(request, 'Imóvel cadastrado com sucesso!')
            return redirect('pagina_inicial')
    else:
        form = ImovelForm()

    return render(request, 'adicionar_imovel.html', {'form': form})


@corretor_required
def editar_imovel(request, id):
    imovel_existente = get_object_or_404(Imovel, id=id)

    if request.method == "POST":
        form = ImovelForm(request.POST, request.FILES, instance=imovel_existente)

        if form.is_valid():
            form.save()

            #Excluir fotos selecionadas
            # Filtra e deleta do banco de dados todas as fotos cujos IDs estão na lista
            fotos_para_excluir = request.POST.getlist('excluir_fotos')
            if fotos_para_excluir:
                  imovel_existente.imagens.filter(id__in=fotos_para_excluir).delete()

            #Adição de novas fotos no carrossel
            novas_imagens = request.FILES.getlist('imagens_adicionais')
            for foto in novas_imagens:
                ImagemImovel.objects.create(imovel=imovel_existente, imagem=foto)

            messages.success(request, 'As alterações do imóvel foram salvas com sucesso!')
            return redirect('pagina_inicial')

    #Quando o usuário entra na tela (Metodo GET)
    else:
          form = ImovelForm(instance=imovel_existente)

    fotos_atuais = imovel_existente.imagens.all()

    dados_para_tela = {
        'form': form,
        'imovel': imovel_existente,
        'fotos': fotos_atuais
    }

    return render(request, 'editar_imovel.html', dados_para_tela)


@corretor_required
@require_POST
def excluir_imovel(request, id):
    imovel_para_deletar = get_object_or_404(Imovel, id=id)
    imovel_para_deletar.delete()
    messages.success(request, 'Imóvel excluído com suceso!')
    return redirect('pagina_inicial')


def detalhes_imovel(request, id):
    imovel = get_object_or_404(Imovel, id=id)
    fotos_adicionais = imovel.imagens.all()

    dados_para_a_tela = {
        'imovel': imovel,
        'fotos': fotos_adicionais
    }

    return render(request, 'detalhes_imovel.html', dados_para_a_tela)


@login_required
def detalhes_perfil(request):
    usuario = request.user
    perfil = None
    tipo_perfil = None

    if hasattr(usuario, 'perfil_cliente'):
        perfil = usuario.perfil_cliente
        tipo_perfil = 'cliente'

    elif hasattr(usuario, 'perfil_corretor'):
        perfil = usuario.perfil_corretor
        tipo_perfil = 'corretor'

    dados_para_tela = {
        'usuario': usuario,
        'perfil': perfil,
        'tipo_perfil': tipo_perfil,
    }

    return render(request, 'detalhes_perfil.html', dados_para_tela)


@login_required
def editar_perfil(request):
    usuario = request.user
    tipo_perfil = None
    perfil_form = None

    if hasattr(usuario, 'perfil_cliente'):
        tipo_perfil = 'cliente'
        perfil_form = ClienteForm(request.POST or None, instance=usuario.perfil_cliente)

    elif hasattr(usuario, 'perfil_corretor'):
        tipo_perfil = 'corretor'
        perfil_form = CorretorForm(request.POST or None, instance=usuario.perfil_corretor)

    else:
        tipo_perfil = 'admin'

    user_form = EditarUsuarioForm(request.POST or None, instance=usuario)

    if request.method == "POST":
        if user_form.is_valid() and (perfil_form is None or perfil_form.is_valid()):
            user_form.save()
            if perfil_form:
                perfil_form.save()

            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('pagina_inicial')

    dados_para_a_tela = {
        'form': user_form,
        'perfil_form': perfil_form,
        'tipo_perfil': tipo_perfil,
        'usuario': usuario
    }
    return render(request, 'editar_perfil.html', dados_para_a_tela)


#Lógica do cadastro
def cadastrar_usuario(request):
    if request.method == "POST":

        form = CadastroUsuarioForm(request.POST)
        tipo_perfil = request.POST.get('tipo_perfil', 'cliente')
        if form.is_valid():
            dados = form.cleaned_data

            usuario = User.objects.create_user(
                username=dados['username'],
                first_name=dados['first_name'],
                email=dados['email'],
                password=dados['password'],
            )

            if tipo_perfil == 'corretor':
                Corretor.objects.create(usuario=usuario, telefone=dados['telefone'])
                messages.success(request, 'Cadastro de Corretor Realizado com Sucesso!')
            else:
                Cliente.objects.create(usuario=usuario, telefone=dados['telefone'])
                messages.success(request, 'Cadastro de Cliente Realizado com Sucesso!')

            login(request, usuario)
            return redirect('pagina_inicial')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário abaixo!')
    else:
        form = CadastroUsuarioForm()

    return render(request, 'cadastro.html', {'form': form})


#lógica do login
def login_usuario(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            usuario = authenticate(username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                messages.success(request, f'Seja bem vindo, {username}!')
                return redirect('pagina_inicial')
        else:
            messages.error(request, 'Não foi possivel realizar o login!\nUsuário e/ou senha inválidos!')
    else:
        if request.user.is_authenticated:
            logout(request)

        form = AuthenticationForm()

    return  render(request, 'login.html', {'form': form})


#Lógica do logout (sair)
def logout_usuario(request):
    logout(request)
    messages.info(request, "Você saiu do sistema!")
    return redirect('login')