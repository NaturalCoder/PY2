from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json
import os


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'mesas.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Mesas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_mesa = db.Column(db.String(100), nullable=False)
    fichas = db.Column(db.Text, nullable=False)


class Fichas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mesa_id = db.Column(db.Integer)
    nome_personagem = db.Column(db.Text, nullable=False)
    classe_personagem = db.Column(db.Text, nullable=False)
    nivel_personagem = db.Column(db.Integer)
    força_personagem = db.Column(db.Integer)
    inteligencia_personagem = db.Column(db.Integer)
    constituicao_personagem = db.Column(db.Integer)
    armadura_personagem = db.Column(db.Integer)
    ataques_personagem = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()  
    if not Mesas.query.filter_by(nome_mesa="ROOM INICIAL").first():
        mesas = Mesas(nome_mesa="ROOM INICIAL", fichas=json.dumps([
        {"id": 1, "nome": "Romulo"},
        {"id": 2, "nome": "Alexandre"}
        ]))
        db.session.add(mesas)
        db.session.commit()

        ficha_romulo = Fichas(
        id=1,
        mesa_id=1,
        nome_personagem="Romulo",
        classe_personagem="Guerreiro",
        nivel_personagem=1,
        força_personagem=10,
        inteligencia_personagem=8,
        constituicao_personagem=12,
        armadura_personagem=5,
        ataques_personagem=json.dumps([
                {
                "arma": "espada",
                "bonos": 4,
                "dado": 8 
                },
                {
                "arma": "besta",
                "bonos": 3,
                "dado": 6 
                }
            ])
        )

        ficha_alexandre = Fichas(
            id=2,
            mesa_id=1,
            nome_personagem="Alexandre",
            classe_personagem="Mago",
            nivel_personagem=1,
            força_personagem=5,
            inteligencia_personagem=18,
            constituicao_personagem=10,
            armadura_personagem=2,
            ataques_personagem=json.dumps([
                {
                "arma": "bola de fogo",
                "bonos": 0,
                "dado": 12 
                },
                {
                "arma": "raio de gelo",
                "bonos": 3,
                "dado": 6 
                }
            ])
        )

        # Adiciona as fichas ao banco de dados
        db.session.add(ficha_romulo)
        db.session.add(ficha_alexandre)
        db.session.commit()

@app.route('/')
def home():

    mesas = Mesas.query.all()

    for mesa in mesas:
        mesa.fichas = json.loads(mesa.fichas)
    
    return render_template('index.html', mesas=mesas)


@app.route('/mesa/<mesa_id>', methods=['GET' , 'POST'])
def mesa(mesa_id):

    if request.method == 'POST':
        new_mesa = Mesas(nome_mesa = request.form['nome_mesa'], fichas=json.dumps([]))
        db.session.add(new_mesa)
        db.session.commit()
        mesa_id = new_mesa.id


    mesa = Mesas.query.get_or_404(mesa_id)

    # Converte a string JSON em um objeto Python (lista de dicionários)
    try:
        fichas_ids = json.loads(mesa.fichas) if mesa.fichas else []
    except json.JSONDecodeError as e:
        fichas_ids = []
        print(f"Erro ao decodificar o JSON da mesa: {e}")

    # Buscar todas as fichas completas pelo ID
    fichas = Fichas.query.filter(Fichas.id.in_([f['id'] for f in fichas_ids])).all()

    # Converter ataques de JSON para lista de dicionários
    for ficha in fichas:
        try:
            ficha.ataques_personagem = json.loads(ficha.ataques_personagem) if ficha.ataques_personagem else []
        except json.JSONDecodeError as e:
            ficha.ataques_personagem = []
            print(f"Erro ao decodificar o JSON dos ataques: {e}")

    return render_template('mesa.html', mesa=mesa, fichas=fichas)

@app.route('/novaFicha/<int:mesa_id>')
def novaFicha(mesa_id):
    return render_template('novaFicha.html', mesa_id = mesa_id)

@app.route('/novaMesa')
def novaMesa():
    return render_template('novaMesa.html')

@app.route('/ficha/<ficha_id>', methods=['GET' , 'POST'])
def ficha(ficha_id):

    if request.method == 'POST':

        ataques = []
        for key in request.form:
            if key.startswith("ataques[") and key.endswith("][arma]"):
                index = key.split("[")[1].split("]")[0]  # Obtém o índice do ataque
                
                arma = request.form.get(f"ataques[{index}][arma]", "").strip()
                bonus = request.form.get(f"ataques[{index}][bonos]", "0").strip()
                dado = request.form.get(f"ataques[{index}][dado]", "0").strip()

                # Converte os valores numéricos corretamente
                ataques.append({
                    "arma": arma,
                    "bonos": int(bonus) if bonus.isdigit() else 0,
                    "dado": int(dado) if dado.isdigit() else 0
                })

        # Converte para JSON formatado
        ataques_json = json.dumps(ataques, ensure_ascii=False, indent=4)

        if ficha_id != "new":

            ficha = Fichas.query.get_or_404(ficha_id)

            ficha.nome_personagem = request.form['nome_personagem']
            ficha.classe_personagem = request.form['classe_personagem']
            ficha.nivel_personagem = request.form['nivel_personagem']
            ficha.força_personagem = request.form['força_personagem']
            ficha.inteligencia_personagem = request.form['inteligencia_personagem']
            ficha.constituicao_personagem = request.form['constituicao_personagem']
            ficha.armadura_personagem = request.form['armadura_personagem']
            ficha.ataques_personagem = ataques_json
            
            db.session.commit()

            try:
                ficha.ataques_personagem = json.loads(ficha.ataques_personagem) if ficha.ataques_personagem else []

            except json.JSONDecodeError as e:
                ficha.ataques_personagem = []
                print(f"Erro ao decodificar o JSON dos ataques: {e}")

            return render_template('ficha.html', ficha=ficha)
                    
        else:

            new_ficha = Fichas(
            mesa_id=request.form['mesa_id'],
            nome_personagem=request.form['nome_personagem'],
            classe_personagem=request.form['classe_personagem'],
            nivel_personagem=request.form['nivel_personagem'],
            força_personagem=request.form['força_personagem'],
            inteligencia_personagem=request.form['inteligencia_personagem'],
            constituicao_personagem=request.form['constituicao_personagem'],
            armadura_personagem=request.form['armadura_personagem'],
            ataques_personagem=ataques_json)
            
            mesa = Mesas.query.get_or_404(new_ficha.mesa_id)

            db.session.add(new_ficha)
            db.session.commit()
            var = {"id": new_ficha.id, "nome": new_ficha.nome_personagem}
            fichas_lista = json.loads(mesa.fichas)
            fichas_lista.append(var)
            mesa.fichas = json.dumps(fichas_lista)

            db.session.commit()

            

            try:
                fichas_ids = json.loads(mesa.fichas) if mesa.fichas else []
            except json.JSONDecodeError as e:
                fichas_ids = []
                print(f"Erro ao decodificar o JSON da mesa: {e}")

            fichas = Fichas.query.filter(Fichas.id.in_([f['id'] for f in fichas_ids])).all()

            for ficha in fichas:
                try:
                    ficha.ataques_personagem = json.loads(ficha.ataques_personagem) if ficha.ataques_personagem else []
                except json.JSONDecodeError as e:
                    ficha.ataques_personagem = []
                    print(f"Erro ao decodificar o JSON dos ataques: {e}")

            return render_template('mesa.html', mesa=mesa, fichas=fichas)
            

    ficha = Fichas.query.get_or_404(ficha_id)

    try:
        ficha.ataques_personagem = json.loads(ficha.ataques_personagem) if ficha.ataques_personagem else []

    except json.JSONDecodeError as e:
        ficha.ataques_personagem = []
        print(f"Erro ao decodificar o JSON dos ataques: {e}")

    return render_template('ficha.html', ficha=ficha)

app.run(debug=True)
