from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Candidato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)

    # Dados pessoais
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    rg = db.Column(db.String(20), unique=True, nullable=False)
    pis = db.Column(db.String(20), unique=True, nullable=False)
    celular = db.Column(db.String(20), nullable=False)
    telefone_recado = db.Column(db.String(20))

    # Dados adicionais
    vaga_pretendida = db.Column(db.String(100), nullable=False)
    trabalhou_na_temon = db.Column(db.String(10))  # Sim/Não
    cidade_estado_nascimento = db.Column(db.String(100))
    data_nascimento = db.Column(db.Date)
    nome_mae = db.Column(db.String(100))
    nome_pai = db.Column(db.String(100))
    
    parente_na_temon = db.Column(db.String(10))  # Sim/Não
    parente_nome = db.Column(db.String(100))
    parente_setor = db.Column(db.String(100))
    
    estado_civil = db.Column(db.String(50))
    cor = db.Column(db.String(50))
    endereco = db.Column(db.String(255))
    bairro = db.Column(db.String(100))
    cidade_estado = db.Column(db.String(100))
    cep = db.Column(db.String(20))
    regiao = db.Column(db.String(100))

    estuda = db.Column(db.String(10))  # Sim/Não
    periodo = db.Column(db.String(50))
    curso = db.Column(db.String(100))

<<<<<<< HEAD

=======
>>>>>>> repositorioprofe/main
    possui_deficiencia = db.Column(db.String(10))  # Sim/Não
    descricao_deficiencia = db.Column(db.String(255))
    data_emissao_rg = db.Column(db.Date)
    estado_expedidor_rg = db.Column(db.String(10))

    # Arquivos
    carteira_trabalho = db.Column(db.String(255))
    certificacao_eletricista = db.Column(db.String(255))
    certificacao_mecanico = db.Column(db.String(255))
    certificado_nr10 = db.Column(db.String(255))

    # Preferências
    horario_diurno = db.Column(db.String(5))
    horario_noturno = db.Column(db.String(5))
    finais_semana = db.Column(db.String(5))

    # Autorização
    autorizo_dados = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Candidato {self.nome}>"
