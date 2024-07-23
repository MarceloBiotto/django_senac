from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from main.bd_config import conecta_no_banco_de_dados
from .forms import ContatoForm
from django.http import HttpResponse
from django.template import loader

def index(request):
    return render(request, 'Guia/index.html')
def sobre(request):
    return render(request, 'Sobre/sobre.html')

def contato(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            try:
                # Estabelecer conexão com o banco de dados
                bd = conecta_no_banco_de_dados()

                # Preparar consulta SQL e valores
                nome = form.cleaned_data['nome']
                email = form.cleaned_data['email']
                mensagem = form.cleaned_data['mensagem']
                sql = "INSERT INTO contatos (nome, email, mensagem) VALUES (%s, %s, %s)"
                values = (nome, email, mensagem)

                # Executar consulta SQL e confirmar alterações
                cursor = bd.cursor()
                cursor.execute(sql, values)
                bd.commit()

                # Mensagem de sucesso e redirecionamento
                print(f"Dados do formulário salvos com sucesso!")
                return HttpResponseRedirect('/')

            except Exception as err:
                # Manipular erros de banco de dados
                print(f"Erro ao salvar dados no banco de dados: {err}")
                mensagem_erro = "Ocorreu um erro ao processar o seu contato. Tente novamente mais tarde."
                return render(request, 'erro.html', mensagem_erro=mensagem_erro), 500

            finally:
                # Fechar conexão com o banco de dados se estiver aberta
                if bd is not None:
                    bd.close()

        else:
            # Manipular dados de formulário inválidos
            return render(request, 'contato.html', {'form': form})

    else:
        # Renderizar formulário vazio
        form = ContatoForm()
        return render(request, 'contato.html', {'form': form})
    
    
    
# @app.route('/login', methods=['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            try:
                # Estabelecer conexão com o banco de dados
                bd = conecta_no_banco_de_dados()

                # Preparar consulta SQL e valores
                nome = form.cleaned_data['nome']
                email = form.cleaned_data['email']
                mensagem = form.cleaned_data['mensagem']
                sql = "INSERT INTO contatos (nome, email, mensagem) VALUES (%s, %s, %s)"
                values = (nome, email, mensagem)

                # Executar consulta SQL e confirmar alterações
                cursor = bd.cursor()
                cursor.execute(sql, values)
                bd.commit()

                # Mensagem de sucesso e redirecionamento
                print(f"Dados do formulário salvos com sucesso!")
                return HttpResponseRedirect('/')

            except Exception as err:
                # Manipular erros de banco de dados
                print(f"Erro ao salvar dados no banco de dados: {err}")
                mensagem_erro = "Ocorreu um erro ao processar o seu contato. Tente novamente mais tarde."
                return render(request, 'erro.html', mensagem_erro=mensagem_erro), 500

            finally:
                # Fechar conexão com o banco de dados se estiver aberta
                if bd is not None:
                    bd.close()

        else:
            # Manipular dados de formulário inválidos
            return render(request, 'Login/login.html', {'form': form})

    else:
        # Renderizar formulário vazio
        form = ContatoForm()
        return render(request, 'Login/login.html', {'form': form})
    

def cadastrar(request):
    if not request.session.get('usuario_id'):
        return redirect('login')
    else:
        if request.method == 'POST':
            nome = request.POST.get('nome')
            email = request.POST.get('email')
            senha = request.POST.get('senha')
          
      
            # Valide a entrada (assumindo lógica de validação)
            if not all([nome, email, senha]):
                # Lide com erros de validação (por exemplo, exiba mensagens de erro)
                return render(request, 'cadastrar.html')

            # Atualize os dados do usuário se a validação for aprovada
            bd = conecta_no_banco_de_dados()
            cursor = bd.cursor()
            sql = (
                """
                INSERT INTO usuarios
                SET nome = %s, email = %s, senha = %s;
                """
            )
            values = (nome, email, senha)
            cursor.execute(sql, values)
            bd.commit()  # Assumindo que você tenha gerenciamento de transações
            cursor.close()
            bd.close()

            # Redirecione para a página de sucesso ou exiba a mensagem de confirmação
            return redirect('sobre') ##envio para a pagina de sobre momentaneamente     

            # Exiba o formulário (assumindo lógica de renderização)
        return render(request, 'Cadastrar/cadastrar.html')            



# @app.route('/validalogin', methods=['POST', 'GET'])
def validaLogin(request):
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')

   
    bd = conecta_no_banco_de_dados()
    cursor = bd.cursor()
    cursor.execute("""
        SELECT *
        FROM contatos
        WHERE nome = %s AND email = %s AND senha = %s;
    """, (nome, email, senha))
    usuario = cursor.fetchone()
    cursor.close()
    bd.close()

    if usuario:
        # Login bem-sucedido
        request.session.get['usuario_id'] = usuario[0]
        request.session.get['usuario_nome'] = usuario[1]
        print(f"{request.session.get['usuario_nome']} logado com sucesso!")
        return render('Sobre/sobre.html') ##enviarei mesmo o login bem sucedito momentaneamente para a pagina sobre, apos isso verificarei alguma forma melhor de organizar essa página
    else:
        # Login inválido
        return render('validaLogin')
  
            
def atualizarUsuario(request,id):
    if not request.session.get('usuario_id'): 
        return redirect('login')
    else:
        id_usuario = id
        bd = conecta_no_banco_de_dados()
        cursor = bd.cursor()
        cursor.execute("""
            SELECT id, nome, email
            FROM usuarios
            WHERE id = %s;
        """, (id,))
        dados_usuario = cursor.fetchone()
        cursor.close()
        bd.close()
        if request.method == 'POST':
            nome = request.POST.get('nome')
            email = request.POST.get('email')
            senha = request.POST.get('senha')    
            if not all([nome, email, senha]):
                return render(request, 'sobre.html')
            bd = conecta_no_banco_de_dados()
            cursor = bd.cursor()
            sql = (
                """
                UPDATE usuarios
                SET nome = %s, email = %s, senha = %s
                WHERE id = %s;
                """
            )
            values = (nome, email, senha, id)
            cursor.execute(sql, values)
            bd.commit()  # Assumindo que você tenha gerenciamento de transações
            cursor.close()
            bd.close()

            # Redirecione para a página de sucesso ou exiba a mensagem de confirmação
            return redirect('paginainicial')     

        # Exiba o formulário (assumindo lógica de renderização)
        return render(request, 'atualizarUsuario.html',{'id': id_usuario})