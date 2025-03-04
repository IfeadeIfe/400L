from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np  # Import NumPy to handle data conversion

app = Flask(__name__)
CORS(app)

# Load your trained model
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json  # Get input from frontend
        text_input = data.get("text", "")

        # Preprocess text
        text_vectorized = vectorizer.transform([text_input])

        # Make prediction
        prediction = model.predict(text_vectorized)[0]
        probability = model.predict_proba(text_vectorized)[0].max()

        # 🔹 Convert NumPy int64 to Python native types
        response = {
            "threat_type": str(prediction),  # Convert to string (if needed)
            "probability": float(probability)  # Convert to float
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    from waitress import serve
    print("🚀 Running Flask with Waitress on port 5000...")
    serve(app, host="0.0.0.0", port=5000)
