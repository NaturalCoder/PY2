from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DateField, FileField, SelectField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError
from validate_docbr import CPF

# Validador customizado de CPF usando a regra matemática nacional
# ✔️ Usamos a validação matemática oficial do CPF: é a mesma regra ensinada pela Receita Federal
# ✔️ É permitido, seguro e aplicável no backend
# ✔️ Não depende de consulta externa e segue o padrão nacional para CPF válido
def validar_cpf(form, field):
    cpf_validador = CPF()
    if not cpf_validador.validate(field.data):
        raise ValidationError("CPF inválido.")

class CandidatoForm(FlaskForm):
    nome = StringField("Nome Completo", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    cpf = StringField("CPF", validators=[DataRequired(), Length(min=11, max=14), validar_cpf])
    rg = StringField("RG", validators=[DataRequired()])
    pis = StringField("PIS", validators=[DataRequired()])
    celular = StringField("Celular", validators=[DataRequired()])
    telefone_recado = StringField("Telefone de Recado", validators=[Optional()])
    vaga_pretendida = StringField("Vaga Pretendida", validators=[DataRequired()])
    trabalhou_na_temon = StringField("Já trabalhou na Temon?", validators=[Optional()])
    cidade_estado_nascimento = StringField("Cidade/Estado de Nascimento", validators=[Optional()])
    data_nascimento = DateField("Data de Nascimento", format="%Y-%m-%d", validators=[Optional()])
    nome_mae = StringField("Nome da Mãe", validators=[Optional()])
    nome_pai = StringField("Nome do Pai", validators=[Optional()])
    parente_na_temon = StringField("Parente na Temon", validators=[Optional()])
    estado_civil = StringField("Estado Civil", validators=[Optional()])
    cor = StringField("Cor", validators=[Optional()])
    endereco = StringField("Endereço", validators=[Optional()])
    bairro = StringField("Bairro", validators=[Optional()])
    cidade_estado = StringField("Cidade e Estado", validators=[Optional()])
    cep = StringField("CEP", validators=[Optional()])
    regiao = StringField("Região", validators=[Optional()])
    estuda = StringField("Estuda?", validators=[Optional()])
    possui_deficiencia = StringField("Possui deficiência?", validators=[Optional()])
    descricao_deficiencia = StringField("Descrição da deficiência e CID", validators=[Optional()])
    data_emissao_rg = DateField("Data de Emissão do RG", format="%Y-%m-%d", validators=[Optional()])
    estado_expedidor_rg = StringField("Estado Expedidor do RG", validators=[Optional()])

    carteira_trabalho = FileField("Carteira de Trabalho (PDF)", validators=[Optional()])
    certificacao_eletricista = FileField("Certificado Eletricista (PDF)", validators=[Optional()])
    certificacao_mecanico = FileField("Certificado Mecânico (PDF)", validators=[Optional()])
    certificado_nr10 = FileField("Certificado NR-10 (PDF)", validators=[Optional()])

    horario_diurno = SelectField("Aceita horário diurno?", choices=[("Sim", "Sim"), ("Não", "Não")])
    horario_noturno = SelectField("Aceita horário noturno?", choices=[("Sim", "Sim"), ("Não", "Não")])
    finais_semana = SelectField("Trabalha nos finais de semana?", choices=[("Sim", "Sim"), ("Não", "Não")])

    autorizo_dados = BooleanField("Autorizo a utilização dos meus dados")
    submit = SubmitField("Enviar")
