from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    city = data.get("city")

    if not city:
        return jsonify({"error": "City is required"}), 400

    try:
        # Fazendo requisição para o wttr.in
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url)
        weather_data = response.json()

        # Extraindo informações do clima
        temp = weather_data["current_condition"][0]["temp_C"]
        description = weather_data["current_condition"][0]["weatherDesc"][0]["value"]
        humidity = weather_data["current_condition"][0]["humidity"]
        wind_speed = weather_data["current_condition"][0]["windspeedKmph"]

        return jsonify({
            "city": city,
            "temperature": f"{temp} °C",
            "description": description.capitalize(),
            "humidity": f"{humidity}%",
            "wind_speed": f"{wind_speed} km/h"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
