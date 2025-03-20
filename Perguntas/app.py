from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alunos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'sua_chave_secreta_super_segura'  # Chave para usar sessions

db = SQLAlchemy(app)

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    pontos = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<Aluno {self.nome}>'

with app.app_context():
    db.create_all()

@app.route('/')
def listar_alunos():
    alunos = Aluno.query.all()
    return render_template('index.html', 
                         alunos=alunos,
                         total_alunos=len(alunos),
                         respondidos=len(session.get('alunos_respondidos', [])))

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_aluno():
    if request.method == 'POST':
        novo_aluno = Aluno(
            nome=request.form['nome'],
            email=request.form['email'],
            idade=int(request.form['idade']),
            pontos=int(request.form['pontos'])
        )
        
        try:
            db.session.add(novo_aluno)
            db.session.commit()
            return redirect(url_for('listar_alunos'))
        except:
            return 'Erro ao cadastrar aluno!'
    return render_template('cadastrar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    if request.method == 'POST':
        aluno.nome = request.form['nome']
        aluno.email = request.form['email']
        aluno.idade = int(request.form['idade'])
        aluno.pontos = int(request.form['pontos'])
        
        try:
            db.session.commit()
            return redirect(url_for('listar_alunos'))
        except:
            return 'Erro ao atualizar aluno!'
    return render_template('editar.html', aluno=aluno)

@app.route('/excluir/<int:id>')
def excluir_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    try:
        db.session.delete(aluno)
        db.session.commit()
        return redirect(url_for('listar_alunos'))
    except:
        return 'Erro ao excluir aluno!'

@app.route('/perguntas', methods=['GET', 'POST'])
def perguntas_sala():
    if 'alunos_respondidos' not in session:
        session['alunos_respondidos'] = []
    
    todos_alunos = Aluno.query.all()
    alunos_disponiveis = [a for a in todos_alunos if a.id not in session['alunos_respondidos']]
    
    if not alunos_disponiveis:
        session['alunos_respondidos'] = []
        alunos_disponiveis = todos_alunos
    
    aluno_selecionado = random.choice(alunos_disponiveis)
    session['alunos_respondidos'].append(aluno_selecionado.id)
    session.modified = True
    
    return render_template('perguntas.html', aluno=aluno_selecionado)

@app.route('/atualizar_pontos/<int:id>/<int:pontos>')
def atualizar_pontos(id, pontos):
    aluno = Aluno.query.get_or_404(id)
    aluno.pontos += pontos
    
    try:
        db.session.commit()
        return redirect(url_for('perguntas_sala'))
    except:
        return 'Erro ao atualizar pontos!'

if __name__ == '__main__':
    app.run(debug=True)