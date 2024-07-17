from django.http import HttpResponseRedirect
from django.shortcuts import render
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
        template = loader.get_template('login.html')
    #     form = ContatoForm(request.POST)
    #     nome = request.form.get('nome')
    #     email = request.form.get('email')
    #     senha = request.form.get('senha')

            
    #     if not nome or not email or not senha:
    #         return redirect(url_for('pagina_login'))

    #     bd = conecta_no_banco_de_dados()
    #     if bd is None:
            
    #      return redirect(url_for('pagina_login'))

    #     cursor = bd.cursor()
    #     try:
    #         cursor.execute("SELECT * FROM contatos WHERE nome=%s AND email=%s AND senha=%s", (nome, email, senha))
    #         user = cursor.fetchone()
    #         if user:
    #             session['usuario_id'] = user[0]
    #             session['usuario_nome'] = user[1]
    #             flash("Login realizado com sucesso.")
    #             return redirect(url_for('index'))
    #         else:
    #             flash("Usuário ou senha incorretos.")
    #     except mysql.connector.Error as err:
    #         flash("Erro ao realizar login: {}".format(err))
    #     finally:
    #         cursor.close()
    #         bd.close()

    return HttpResponse(template.render(request))
    # return render(request, 'login.html')