from flask import Flask, render_template, request
import mensagens

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Obtém o nome do formulário
        nome = request.form.get("nome") # atributo name do formulário
        
        # Gera mensagem
        mensagem = f"Olá {nome}!\nMensagem: {mensagens.obter_mensagem_aleatoria()}"
            
        # Renderiza a página com a mensagem
        return render_template("index.html", texto=mensagem)

    # Renderiza a página inicial com o formulário
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)