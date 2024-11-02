import requests

def buscar_endereco_por_cep(cep):
    try:
        # Remover caracteres especiais do CEP
        cep = cep.replace("-", "").replace(".", "").strip()
    
        # Faz a requisição a API do ViaCEP
        response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        if response.status_code == 200:
            dados = response.json()
            if "erro" in dados:
                return { "erro": "CEP não localizado." }
            return dados
        else:
            return { "erro": "Erro ao consultar o CEP." }
    except Exception as e:
        return { "erro": f"Erro: {str(e)}" }
    
