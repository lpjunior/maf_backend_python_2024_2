from flask import Blueprint, render_template, request, url_for, redirect, session
from services.task_service import TaskService

task_blueprint = Blueprint('task', __name__, url_prefix="/task")
task_service = TaskService()

@task_blueprint.route("/listar")
def listar():
    # Renderiza o template task_list.html com a lista de tarefas
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    
    user_id = session['user_id']
    tarefas = task_service.listar_tarefas(user_id)
    return render_template("task_list.html", tarefas=tarefas)

@task_blueprint.route("/adicionar", methods=["POST"])
def adicionar():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))

    user_id = session['user_id']
    conteudo = request.form.get("tarefa")
    prioridade = request.form.get("prioridade", "Média")
    
    if prioridade == '':
        prioridade = 'Média'

    try:
        task_service.adicionar_tarefa(conteudo, user_id, prioridade)
    except ValueError as e:
        return str(e), 400

    return redirect(url_for("task.listar"))

@task_blueprint.route("/completar/<int:tarefa_id>")
def completar(tarefa_id):
    
    try:
        # Marca a tarefa como completa
        task_service.completar_tarefa(tarefa_id)
    except Exception as e:
        return str(e), 400
    
    return redirect(url_for("task.listar"))

@task_blueprint.route("/remover/<int:tarefa_id>")
def remover(tarefa_id):
    # Remove a tarefa da lista
    try:
        # Marca a tarefa como completa
        task_service.remover_tarefa(tarefa_id)
    except Exception as e:
        return str(e), 400
    
    return redirect(url_for("task.listar"))