from flask import Flask, request, jsonify
import joblib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load your trained model
model = joblib.load("traffic_model.pkl")  # Replace with actual filename if different

@app.route('/predict', methods=['POST'])
def predict():
    try:
        features = request.json['features']  # List of 37 features
        # ✅ Corrected to 40
        if len(features) != 40:
          return jsonify({'error': f'Expected 40 features, got {len(features)}'}), 400

        prediction = model.predict([features])[0]
        return jsonify({'prediction': float(prediction)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
