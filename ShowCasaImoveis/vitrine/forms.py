from django import forms
from django.contrib.auth.models import User
from .models import Imovel, Corretor, Cliente


#Formulário do imovel (para cadastrar e editar)
class ImovelForm(forms.ModelForm):
    class Meta:
        model = Imovel
        exclude = ['corretor']

        # Criamos as opções para o Select
        OPCOES_IMOVEL = [
            ('', 'Escolha...'),
            ('Casa', 'Casa'),
            ('Apartamento', 'Apartamento'),
            ('Terreno', 'Terreno'),
            ('Comercial', 'Ponto Comercial'),
        ]

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Casa Duplex Moderna com Piscina'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Fale sobre os cômodos, acabamentos, diferenciais...'}),
            'tipo_imovel': forms.Select(choices=OPCOES_IMOVEL, attrs={'class': 'form-select'}),
            'ano_construcao': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 2026'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 450000.00'}),

            'logradouro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Av. Paulista'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 123'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Centro'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: São Paulo'}),

            'imagem_principal': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }


#Formulario de cadastro de usuário
class CadastroUsuarioForm(forms.ModelForm):
    first_name = forms.CharField(label="Nome Completo",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu nome completo'}))
    #Capturando o telefone temporariamente (depois vou utilizar na views)
    telefone = forms.CharField(label="Telefone",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(DD) 99999-9999'}))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Cadastre uma senha'}))
    password_confirm = forms.CharField(label="Confirmar Senha",widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme sua senha'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'exemplo@gmail.com'}),
        }

    #Verificando se as senhas combinam
    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("password")
        confirmacao = cleaned_data.get("password_confirm")

        if senha and confirmacao and senha != confirmacao:
            raise forms.ValidationError("A senha e a confirmação devem ser iguais!")
        return cleaned_data


#Formulário para edição dos dados do usuário
class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


#Formulario especifico para alterar os dados do modelo corretor
class CorretorForm(forms.ModelForm):
    class Meta:
        model = Corretor
        fields = ['telefone']
        widgets = {
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(DD) 99999-9999'}),
        }


#Formulario especifico para alterar os dados do modelo cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['telefone']
        widgets = {
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(DD) 99999-9999'}),
        }
