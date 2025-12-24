from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Docker ağındaki diğer servisin adresi
WEATHER_SERVICE_URL = "http://weather-service:5001/weather"

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    recommendation = None
    city = None
    error = None

    if request.method == 'POST':
        city = request.form.get('city')
        
        # 1. Hava Durumu Servisine İstek At
        try:
            response = requests.get(f"{WEATHER_SERVICE_URL}/{city}")
            if response.status_code == 200:
                weather_data = response.json()
            else:
                error = "Şehir bulunamadı veya servis hatası."
        except:
            error = "Hava durumu servisine ulaşılamıyor."

        # 2. Eğer veri geldiyse Öneri Mantığını Çalıştır
        if weather_data:
            temp = weather_data.get('temp')
            condition = weather_data.get('condition')

            if condition == "rainy":
                recommendation = "☔ Şemsiyeni al ve su geçirmez bot giy."
            elif condition == "snowy":
                recommendation = "❄️ Çok soğuk! Atkı, bere ve eldiven şart."
            elif temp > 20:
                recommendation = "😎 Hava harika, tişört ve güneş gözlüğü yeterli."
            else:
                recommendation = "🧥 Hava biraz serin olabilir, yanına bir hırka al."

    return render_template('index.html', city=city, weather=weather_data, recommendation=recommendation, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
