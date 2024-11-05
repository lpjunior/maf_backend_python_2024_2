import requests
import time


def get_coordinates_from_address(cep):
    url = f'https://nominatim.openstreetmap.org/search'
    params = {
        'q':cep,
        'format': 'jsonv2'
    }
    headers = {
        'User-Agent': 'Alugueis/1.0 (luis@senac.com.br)'
    }
    max_retries=3
    delay=2
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, headers=headers)

            if response.status_code == 200:
                data = response.json()
                if data:
                    location = data[0]
                    return location['lat'], location['lon'], location['display_name']
                else:
                    print(f"Resposta vazia da Nominatim. Tentativa {attempt + 1} de {max_retries}.")
            else:
                print(f'Erro ao buscar coordenadas. Status: {response.status_code} - {response.reason}. Tentativa {attempt + 1} de {max_retries}.')
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}. Tentativa {attempt + 1} de {max_retries}.")
        
        time.sleep(delay)

    print("Todas as tentativas falharam. Tente novamente mais tarde.")
    return None, None, None