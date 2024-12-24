from flask import Flask, render_template, request, jsonify
import json
import os
from fuzzywuzzy import process  # Fuzzywuzzy kütüphanesini ekliyoruz

app = Flask(__name__)

def load_responses():
    responses_path = os.path.join(os.path.dirname(__file__), "responses", "response.json")
    with open(responses_path, "r", encoding="utf-8") as file:
        return json.load(file)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form["user_input"]
    
    # Yanıtları yükle
    responses = load_responses()

    best_match = None
    highest_score = 0

    # Kullanıcı inputuna göre yanıtları arayın
    for category in responses.values():
        for sub_topic, data in category["alt_konular"].items():
            # Fuzzywuzzy ile en iyi eşleşmeyi buluyoruz
            match = process.extractOne(user_input, data["keywords"])
            if match and match[1] > highest_score:  # match[1] eşleşme oranını içerir
                highest_score = match[1]    
                best_match = data

    if best_match and highest_score >= 50:  # Eğer eşleşme oranı 50'den yüksekse
        return jsonify({"response": best_match["response"]})

    return jsonify({"response": "Üzgünüm, bu konuda bir bilgi bulamadım."}) 

if __name__ == "__main__":
    app.run(debug=True) 
