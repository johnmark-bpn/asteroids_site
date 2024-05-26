from flask import Flask, render_template
import requests
import datetime

app = Flask(__name__)

def get_neo_data(api_key):
    # URL base da API NeoWs
    base_url = "https://api.nasa.gov/neo/rest/v1/feed"

    # Data atual no formato YYYY-MM-DD
    today_date = datetime.date.today().strftime('%Y-%m-%d')

    # Parâmetros para a requisição
    params = {
        'start_date': today_date,
        'end_date': today_date,
        'api_key': api_key
    }

    try:
        # Fazendo a requisição GET à API
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Levanta uma exceção para códigos de status 4xx/5xx

        # Processando a resposta
        data = response.json()

        # Verificando se a chave 'near_earth_objects' está presente
        if 'near_earth_objects' not in data:
            return []

        near_earth_objects = data['near_earth_objects'].get(today_date, [])

        asteroid_data = []
        for neo in near_earth_objects:
            name = neo.get('name', 'N/A')
            magnitude = neo.get('absolute_magnitude_h', 'N/A')
            diameter = neo.get('estimated_diameter', {}).get('meters', {}).get('estimated_diameter_max', 'N/A')
            hazardous = neo.get('is_potentially_hazardous_asteroid', False)

            asteroid_data.append({
                'name': name,
                'magnitude': magnitude,
                'diameter': diameter,
                'hazardous': hazardous
            })

        return asteroid_data

    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer requisição à API: {e}")
        return []


@app.route('/')
def index():
    # Substitua 'YOUR_API_KEY' pela sua chave de API da NASA
    api_key = 'GM5UuVoJHYtRgXzzpevgsGilVuEDGSDRcRopCXW5'
    neo_data = get_neo_data(api_key)
    return render_template('index.html', neo_data=neo_data)

if __name__ == "__main__":
    app.run(debug=True)

