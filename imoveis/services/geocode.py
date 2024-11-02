import requests

def get_coordinates_from_address(cep):
    url = f'https://nominatim.openstreetmap.org/search'
    params = {
        'q':cep,
        'format': 'jsonv2'
    }
    headers = {
        'User-Agent': 'Alugueis/1.0 (luis@senac.com.br)'
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200 and response.json():
        location = response.json()[0]
        return location['lat'], location['lon'], location['display_name']
    else:
        print('Erro ao buscar coordenadas.')
        return None, None, None