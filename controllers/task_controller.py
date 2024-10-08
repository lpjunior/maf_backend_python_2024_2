from flask import Blueprint, render_template, request, url_for, redirect
from services.task_service import TaskService

task_blueprint = Blueprint('task', __name__)
task_service = TaskService()

@task_blueprint.route("/")
def index():
    # Renderiza o template index.html com a lista de tarefas
    tarefas = task_service.listar_tarefas()
    return render_template("index.html", tarefas=tarefas)

@task_blueprint.route("/adicionar", methods=["POST"])
def adicionar():
    conteudo = request.form.get("tarefa")
    prioridade = request.form.get("prioridade", "Média")

    try:
        task_service.adicionar_tarefa(conteudo, prioridade)
    except ValueError as e:
        return str(e), 400

    return redirect(url_for("task.index"))

@task_blueprint.route("/completar/<int:tarefa_id>")
def completar(tarefa_id):
    
    try:
        # Marca a tarefa como completa
        task_service.completar_tarefa(tarefa_id)
    except Exception as e:
        return str(e), 400
    
    return redirect(url_for("task.index"))

@task_blueprint.route("/remover/<int:tarefa_id>")
def remover(tarefa_id):
    # Remove a tarefa da lista
    try:
        # Marca a tarefa como completa
        task_service.remover_tarefa(tarefa_id)
    except Exception as e:
        return str(e), 400
    
    return redirect(url_for("task.index"))