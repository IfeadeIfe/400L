from flask import Flask, request, jsonify
import joblib  # For loading ML model
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

model = joblib.load("model.pkl")  
vectorizer = joblib.load("vectorizer.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        text_input = data.get("text", "")

  
        text_vectorized = vectorizer.transform([text_input])
        prediction = model.predict(text_vectorized)[0]
        probability = model.predict_proba(text_vectorized)[0].max()

        return jsonify({"threat_type": prediction, "probability": float(probability)})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
