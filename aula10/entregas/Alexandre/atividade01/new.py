from flask import Flask, render_template, request, redirect, url_for, session, flash
import hashlib, json

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Necessário para sessões e mensagens flash

# Função para calcular o hash SHA-256 de uma senha
def calcular_hash(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Função para carregar a lista de usuários de um arquivo JSON
def carregar_usuarios(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        usuarios = json.load(arquivo)
    return usuarios

# Carregar usuários do arquivo JSON
usuarios = carregar_usuarios('usuarios.json')

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        hash_senha = calcular_hash(senha)

        if usuario in usuarios and usuarios[usuario] == hash_senha:
            session['usuario_logado'] = usuario
            return redirect(url_for('sucesso'))
        else:
            flash('Credenciais inválidas. Tente novamente!', 'error')
    
    return render_template('login.html')


    
@appusuario_logado
def sua_funcao():
    if session:
        return render_template('sucesso.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
    
    
# ///////////////////////////////////////////////////////////////////////////////////////////////////////

# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
import hashlib, json

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Necessário para sessões e mensagens flash

# Função para calcular o hash SHA-256 de uma senha
def calcular_hash(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Função para carregar a lista de usuários de um arquivo JSON
def carregar_usuarios(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        usuarios = json.load(arquivo)
    return usuarios

# Carregar usuários do arquivo JSON
usuarios = carregar_usuarios('usuarios.json')

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        hash_senha = calcular_hash(senha)

        if usuario in usuarios and usuarios[usuario] == hash_senha:
            session['usuario_logado'] = usuario
            return redirect(url_for('sucesso'))
        else:
            flash('Credenciais inválidas. Tente novamente!', 'error')
    
    return render_template('login.html')

@app.route('/sucesso')
def sucesso():
    if 'usuario_logado' in session:
        return render_template('sucesso.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)