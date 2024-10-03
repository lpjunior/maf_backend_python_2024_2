from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

# Lista de tarefas em memória
tarefas = []

@app.route("/")
def index():
    # Renderiza o template index.html com a lista de tarefas
    return render_template("index.html", tarefas=tarefas)

@app.route("/adicionar", methods=["POST"])
def adicionar():
    nova_tarefa = request.form.get("tarefa")
    
    # Adiciona a nova tarefa à lista
    if nova_tarefa:
        tarefa = {"conteudo": nova_tarefa, "completa": False}
        tarefas.append(tarefa)
    
    return redirect(url_for("index"))

@app.route("/completar/<int:tarefa_id>")
def completar(tarefa_id):
    # Marca a tarefa como completa
    tarefas[tarefa_id]["completa"] = True
    return redirect(url_for("index"))

@app.route("/remover/<int:tarefa_id>")
def remover(tarefa_id):
    # Remove a tarefa da lista
    tarefas.pop(tarefa_id)
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)