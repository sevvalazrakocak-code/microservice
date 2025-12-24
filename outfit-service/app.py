from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Docker içinde diğer servisin adı "weather-service" olacak (docker-compose'da tanımladığımız isim)
WEATHER_SERVICE_URL = "http://weather-service:5001/weather"

@app.route('/recommend', methods=['GET'])
def recommend():
    city = request.args.get('city')
    
    if not city:
        return jsonify({"error": "Lutfen ?city=sehiradi seklinde sehir girin"}), 400

    # Adım 1: Diğer servise (Microservice Communication) istek at
    try:
        response = requests.get(f"{WEATHER_SERVICE_URL}/{city}")
        weather_data = response.json()
    except:
        return jsonify({"error": "Hava durumu servisine ulasilamadi"}), 503

    temp = weather_data.get('temp')
    condition = weather_data.get('condition')
    outfit = ""

    # Adım 2: İş Mantığı (Business Logic)
    if condition == "rainy":
        outfit = "Şemsiyeni al ve su geçirmez bot giy."
    elif condition == "snowy":
        outfit = "Çok soğuk! Atkı, bere ve eldiven şart."
    elif temp > 20:
        outfit = "Hava harika, tişört ve güneş gözlüğü yeterli."
    else:
        outfit = "Hava biraz serin olabilir, yanına bir hırka al."

    # Adım 3: Sonucu Dön
    return jsonify({
        "city": city,
        "weather_report": weather_data,
        "recommendation": outfit
    })

if __name__ == '__main__':
    # Bu servis 5002 portunda çalışacak
    app.run(host='0.0.0.0', port=5002)
