from flask import Flask, jsonify

app = Flask(__name__)

# Mock Database (Sanki dışarıdan veya DB'den geliyormuş gibi)
weather_data = {
    "istanbul": {"temp": 14, "condition": "rainy"},
    "ankara": {"temp": 5, "condition": "snowy"},
    "izmir": {"temp": 22, "condition": "sunny"},
    "london": {"temp": 8, "condition": "cloudy"}
}

@app.route('/weather/<city>', methods=['GET'])
def get_weather(city):
    city_key = city.lower()
    # Şehir yoksa varsayılan bir değer dön
    data = weather_data.get(city_key, {"temp": 20, "condition": "unknown"})
    return jsonify(data)

if __name__ == '__main__':
    # Bu servis 5001 portunda çalışacak
    app.run(host='0.0.0.0', port=5001)
