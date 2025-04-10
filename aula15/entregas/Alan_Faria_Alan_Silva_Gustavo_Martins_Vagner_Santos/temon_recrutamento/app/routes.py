from flask import Blueprint, render_template, request, redirect, url_for, current_app
from app.models import db, Candidato
from app.forms import CandidatoForm
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import time

# Blueprint nomeado como "app" (usado no url_for('app.alguma_rota'))
main_routes = Blueprint("app", __name__)

def salvar_arquivo(arquivo):
    if arquivo and arquivo.filename:
        filename = secure_filename(arquivo.filename)
        timestamp = str(int(time.time()))
        pasta_uploads = current_app.config.get("UPLOAD_FOLDER", "uploads")
        os.makedirs(pasta_uploads, exist_ok=True)
        caminho_completo = os.path.join(pasta_uploads, f"{timestamp}_{filename}")
        arquivo.save(caminho_completo)
        return caminho_completo
    return None

@main_routes.route("/", methods=["GET", "POST"])
def formulario():
    form = CandidatoForm()

    if form.validate_on_submit():
        candidato = Candidato(
            nome=form.nome.data,
            email=form.email.data,
            cpf=form.cpf.data,
            rg=form.rg.data,
            pis=form.pis.data,
            celular=form.celular.data,
            telefone_recado=form.telefone_recado.data,
            vaga_pretendida=form.vaga_pretendida.data,
            trabalhou_na_temon=form.trabalhou_na_temon.data,
            cidade_estado_nascimento=form.cidade_estado_nascimento.data,
            data_nascimento=form.data_nascimento.data,
            nome_mae=form.nome_mae.data,
            nome_pai=form.nome_pai.data,
            parente_na_temon=form.parente_na_temon.data,
            parente_nome=form.nome_parente.data,
            parente_setor=form.setor_parente.data,
            estado_civil=form.estado_civil.data,
            cor=form.cor.data,
            endereco=form.endereco.data,
            bairro=form.bairro.data,
            cidade_estado=form.cidade_estado.data,
            cep=form.cep.data,
            regiao=form.regiao.data,
            estuda=form.estuda.data,
            curso=form.curso.data,
            periodo=form.periodo.data,
            possui_deficiencia=form.possui_deficiencia.data,
            descricao_deficiencia=form.descricao_deficiencia.data,
            data_emissao_rg=form.data_emissao_rg.data,
            estado_expedidor_rg=form.estado_expedidor_rg.data,
            carteira_trabalho=salvar_arquivo(request.files.get("carteira_trabalho")),
            certificacao_eletricista=salvar_arquivo(request.files.get("certificacao_eletricista")),
            certificacao_mecanico=salvar_arquivo(request.files.get("certificacao_mecanico")),
            certificado_nr10=salvar_arquivo(request.files.get("certificado_nr10")),
            horario_diurno=form.horario_diurno.data,
            horario_noturno=form.horario_noturno.data,
            finais_semana=form.finais_semana.data,
            autorizo_dados=form.autorizo_dados.data
        )

        db.session.add(candidato)
        db.session.commit()
        return redirect(url_for("app.confirmacao"))

    return render_template("formulario.html", form=form)

@main_routes.route("/confirmacao")
def confirmacao():
    return render_template("confirmacao.html")
