Projeto: Show Case Imoveis
Projeto em python, utilizando Django, de uma vitrine de imóveis disponíveis para venda. 
Feito com: python, django, bootstrap, HTML, CSS, JS, banco relacional estruturado e configuracoes basicas de seguranca.

Para rodar o projeto corretamente em sua máquina, siga o passo a passo a seguir.

Abra o terminal e digite:

#Para criar o ambiente virtual
python -m venv .venv

#Para ativar o ambiente virtual
venv\Scripts\activate

#Para instalar as configurações utilizadas no projeto
pip install -r requirements.txt

#Entrando no diretório certo
caso esteja na pasta raiz (ShowCaseImoveis), vá para a pasta "ShowCasaImoveis" (utilizando o comando: cd .\ShowcasaImoveis\) 

#Fazendo a migração do modelo para o banco de dados
manage.py migrate

#Rodar o servidor
python manage.py runserver
