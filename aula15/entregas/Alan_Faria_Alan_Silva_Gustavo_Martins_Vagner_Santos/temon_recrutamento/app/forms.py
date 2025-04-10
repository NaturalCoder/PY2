from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DateField, FileField, SelectField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError
from validate_docbr import CPF

def validar_cpf(form, field):
    cpf_validador = CPF()
    if not cpf_validador.validate(field.data):
        raise ValidationError("CPF inválido.")

# Lista com todos os estados do Brasil
ESTADOS_BRASIL = [
    ("", "---"), ("AC", "Acre"), ("AL", "Alagoas"), ("AP", "Amapá"), ("AM", "Amazonas"), ("BA", "Bahia"),
    ("CE", "Ceará"), ("DF", "Distrito Federal"), ("ES", "Espírito Santo"), ("GO", "Goiás"), ("MA", "Maranhão"),
    ("MT", "Mato Grosso"), ("MS", "Mato Grosso do Sul"), ("MG", "Minas Gerais"), ("PA", "Pará"),
    ("PB", "Paraíba"), ("PR", "Paraná"), ("PE", "Pernambuco"), ("PI", "Piauí"), ("RJ", "Rio de Janeiro"),
    ("RN", "Rio Grande do Norte"), ("RS", "Rio Grande do Sul"), ("RO", "Rondônia"), ("RR", "Roraima"),
    ("SC", "Santa Catarina"), ("SP", "São Paulo"), ("SE", "Sergipe"), ("TO", "Tocantins")
]

class CandidatoForm(FlaskForm):
    nome = StringField("Nome Completo", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    cpf = StringField("CPF", validators=[DataRequired(), Length(min=11, max=14), validar_cpf])
    rg = StringField("RG", validators=[DataRequired()])
    pis = StringField("PIS", validators=[DataRequired()])
    celular = StringField("Celular", validators=[DataRequired()])
    telefone_recado = StringField("Telefone de Recado", validators=[Optional()])
    vaga_pretendida = StringField("Vaga Pretendida", validators=[DataRequired()])
    trabalhou_na_temon = SelectField("Já trabalhou na Temon?", choices=[("Sim", "Sim"), ("Não", "Não")])

    estado_nascimento = SelectField("Estado de Nascimento", choices=ESTADOS_BRASIL, validators=[Optional()])
    cidade_nascimento = StringField("Cidade de Nascimento", validators=[Optional()])

    data_nascimento = DateField("Data de Nascimento", format="%Y-%m-%d", validators=[Optional()])
    nome_mae = StringField("Nome da Mãe", validators=[Optional()])
    nome_pai = StringField("Nome do Pai", validators=[Optional()])

    parente_na_temon = SelectField("Parente na Temon", choices=[("Sim", "Sim"), ("Não", "Não")])
    nome_parente = StringField("Nome do Parente", validators=[Optional()])
    setor_parente = StringField("Setor do Parente", validators=[Optional()])

    estado_civil = SelectField("Estado Civil", choices=[
        ("Solteiro(a)", "Solteiro(a)"), ("Casado(a)", "Casado(a)"),
        ("Divorciado(a)", "Divorciado(a)"), ("Viúvo(a)", "Viúvo(a)")
    ])

    cor = StringField("Cor", validators=[Optional()])
    endereco = StringField("Endereço", validators=[Optional()])
    bairro = StringField("Bairro", validators=[Optional()])
    cidade_estado = StringField("Cidade e Estado", validators=[Optional()])
    cep = StringField("CEP", validators=[Optional()])
    regiao = StringField("Região", validators=[Optional()])

    estuda = SelectField("Estuda?", choices=[("Sim", "Sim"), ("Não", "Não")])
    curso = StringField("Curso", validators=[Optional()])
    periodo = StringField("Período", validators=[Optional()])

    possui_deficiencia = StringField("Possui deficiência?", validators=[Optional()])
    descricao_deficiencia = StringField("Descrição da deficiência e CID", validators=[Optional()])
    data_emissao_rg = DateField("Data de Emissão do RG", format="%Y-%m-%d", validators=[Optional()])
    estado_expedidor_rg = StringField("Estado Expedidor do RG", validators=[Optional()])

    carteira_trabalho = FileField("Carteira de Trabalho", validators=[Optional()])
    certificacao_eletricista = FileField("Certificado Eletricista", validators=[Optional()])
    certificacao_mecanico = FileField("Certificado Mecânico", validators=[Optional()])
    certificado_nr10 = FileField("Certificado NR-10", validators=[Optional()])

    horario_diurno = SelectField("Aceita horário diurno?", choices=[("Sim", "Sim"), ("Não", "Não")])
    horario_noturno = SelectField("Aceita horário noturno?", choices=[("Sim", "Sim"), ("Não", "Não")])
    finais_semana = SelectField("Trabalha nos finais de semana?", choices=[("Sim", "Sim"), ("Não", "Não")])

    autorizo_dados = BooleanField("Autorizo a utilização dos meus dados")
    submit = SubmitField("Enviar")
