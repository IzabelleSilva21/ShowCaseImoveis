from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.decorators.http import require_POST


from .models import *

#Criar um metodo group para poder colocar a lógica de ser o tipo corretor e estar logado (utilizar no adicionar_imovel)

def pagina_inicial(request):
    lista_imoveis = Imovel.objects.all()
    return render(request, 'pagina_inicial.html', {'imoveis': lista_imoveis})


@login_required
def adicionar_imovel(request):

    #Aqui só usuários do tipo corretor podem adicionar imóveis
    if not hasattr(request.user, 'perfil_corretor'):
        messages.error(request, 'Apenas corretores podem adicionar imóveis!')
        return redirect('pagina_inicial')

    if request.method == "POST":
        v_titulo = request.POST.get('titulo')
        v_descricao = request.POST.get('descricao')
        v_tipo = request.POST.get('tipo_Imovel')
        v_ano = request.POST.get('ano_construcao')
        v_preco = request.POST.get('preco')
        v_logradouro = request.POST.get('logradouro')
        v_numero = request.POST.get('numero')
        v_bairro = request.POST.get('bairro')
        v_cidade = request.POST.get('cidade')

        #imagem principal
        v_imagem = request.FILES.get('imagem_principal')

        novo_imovel = Imovel(
            titulo=v_titulo,
            descricao=v_descricao,
            tipo_Imovel=v_tipo,
            ano_construcao=v_ano,
            preco=v_preco,
            logradouro=v_logradouro,
            numero=v_numero,
            bairro=v_bairro,
            cidade=v_cidade,
            imagem_principal=v_imagem,
            corretor=request.user
        )
        novo_imovel.save()

        #Captura a lista de imagens adicionais
        imagens_adicionais = request.FILES.getlist('imagens_adicionais')
        for foto in imagens_adicionais:
            ImagemImovel.objects.create(
                imovel=novo_imovel,
                imagem=foto
            )
        messages.success(request, 'Imóvel cadastrado com sucesso!')
        return redirect('pagina_inicial')

    return render(request, 'adicionar_imovel.html')

@login_required
def editar_imovel(request, id):
    imovel_existente = get_object_or_404(Imovel, id=id)

    if imovel_existente.corretor != request.user:
        messages.error(request, 'Você não tem permissão para realizar essa ação! \nApenas o corretor responsável pode editar esse imóvel!')
        return redirect('pagina_inicial')

    if request.method == "POST":
        imovel_existente.titulo = request.POST.get('titulo')
        imovel_existente.descricao = request.POST.get('descricao')
        imovel_existente.tipo_Imovel = request.POST.get('tipo_Imovel')
        imovel_existente.ano_construcao = request.POST.get('ano_construcao')
        imovel_existente.preco = request.POST.get('preco')
        imovel_existente.logradouro = request.POST.get('logradouro')
        imovel_existente.numero = request.POST.get('numero')
        imovel_existente.bairro = request.POST.get('bairro')
        imovel_existente.cidade = request.POST.get('cidade')

        # Atualizando a imagem de capa (se enviada)
        if request.FILES.get('imagem_principal'):
            imovel_existente.imagem_principal = request.FILES.get('imagem_principal')

        imovel_existente.save()

        #Excluir fotos selecionadas
        fotos_para_excluir = request.POST.getlist('excluir_fotos')
        if fotos_para_excluir:
            # Filtra e deleta do banco de dados todas as fotos cujos IDs estão na lista
            imovel_existente.imagens.filter(id__in=fotos_para_excluir).delete()

        #Adição de novas fotos no carrossel
        # Captura os múltiplos arquivos enviados pelo input name="imagens_adicionais"
        novas_imagens = request.FILES.getlist('imagens_adicionais')
        for foto in novas_imagens:
            # Cria um registro no modelo secundário vinculando a foto a este imóvel
            ImagemImovel.objects.create(imovel=imovel_existente, imagem=foto)

        messages.success(request, 'As alterações do imóvel foram salvas com sucesso!')
        return redirect('pagina_inicial')

    fotos_atuais = imovel_existente.imagens.all()

    # Criando o dicionário de contexto
    dados_para_tela = {
        'imovel': imovel_existente,
        'fotos': fotos_atuais
    }

    # Passando o dicionário para a função render
    return render(request, 'editar_imovel.html', dados_para_tela)


@login_required
@require_POST
def excluir_imovel(request, id):
    imovel_para_deletar = get_object_or_404(Imovel, id=id)

    if imovel_para_deletar.corretor != request.user:
        messages.error(request, 'Você não tem permissão para realizar essa operação!\nApenas o corretor responsável pode excluir esse imóvel!')
        return redirect('pagina_inicial')


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


@login_required     #Só quem tá logado pode acessar essa função
def editar_perfil(request):
    usuario = request.user
    perfil = None
    tipo_perfil = None

    if hasattr(usuario, 'perfil_cliente'):
        perfil = usuario.perfil_cliente
        tipo_perfil = 'cliente'
    elif hasattr(usuario, 'perfil_corretor'):
        perfil = usuario.perfil_corretor
        tipo_perfil = 'corretor'

    if request.method == "POST":
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')
        usuario.save()

        if perfil:
            perfil.telefone = request.POST.get('telefone')
            perfil.save()
        return redirect('pagina_inicial')

    dados_para_a_tela = {
        'usuario': usuario,
        'perfil': perfil,
        'tipo_perfil': tipo_perfil
    }
    return render(request, 'editar_perfil.html', dados_para_a_tela)


#Lógica do cadastro
def cadastrar_usuario(request):
    if request.method == "POST":
        # Capturando os dados que vieram do formulário limpo do HTML
        usuario_input = request.POST.get('username')
        email_input = request.POST.get('email')
        telefone_usuario = request.POST.get('telefone')
        tipo_usuario = request.POST.get('tipo_usuario', 'cliente')
        senha_input = request.POST.get('password')
        confirmacao_senha = request.POST.get('password_confirm')

        # Validação simples: verifica se as senhas são iguais
        if senha_input != confirmacao_senha:
            messages.error(request, 'A senha e a confirmação devem ser iguais!')
            return render(request, 'cadastro.html')

        # Validação simples: verifica se o usuário já existe
        if User.objects.filter(username=usuario_input).exists():
            messages.error(request, 'Este nome de usuário já está em uso.')
            return render(request, 'cadastro.html')

        # 1. Cria o Usuário padrão do Django criptografando a senha de forma segura
        usuario = User.objects.create_user(username=usuario_input, email=email_input, password=senha_input)

        # 2. Vincula ao Perfil correspondente (Corretor ou Cliente)
        if tipo_usuario == 'corretor':
            Corretor.objects.create(usuario=usuario, telefone=telefone_usuario)
            # PARA TESTAR SE TÁ CADASTRANDO CERTO
            messages.success(request, 'Cadastro de Corretor Realizado com Sucesso!')
        else:
            Cliente.objects.create(usuario=usuario, telefone=telefone_usuario)
            messages.success(request, 'Cadastro de Cliente Realizado com Sucesso!')

        # 3. Loga o usuário automaticamente e redireciona
        login(request, usuario)
        messages.success(request, 'Cadastro Realizado com Sucesso!')
        return redirect('pagina_inicial')

    return render(request, 'cadastro.html')


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