from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tarefas.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dados = db.Column(db.Text, nullable=False)
    
with app.app_context():
    db.create_all()
    tarefa = Tarefa(dados="{}")
    db.session.add(tarefa)
    db.session.commit()

@app.route('/')
def home():
    return render_template('tarefas.html')


@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        # request.form[0]
        # request.form['descricaoTarefa']
        # request.form['duracaoTarefa']
        tarefa = Tarefa.query.get(0)
        tarefa.dados = request.data
        
        try:
            db.session.commit()
            return { 'result': 'OK cadastrado' }
        except:
            return { 'result': 'Erro ao cadastrar tarefa' }
    else:
        tarefa = Tarefa.query.get(0)
        return tarefa.dados

app.run(debug=True)
