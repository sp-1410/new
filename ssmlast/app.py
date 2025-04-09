from flask import Flask, render_template, request, jsonify
import re
from urllib.parse import urlparse
from model.predict import predict_url, extract_features

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    url = data.get('url', '')
    
    # Make sure URL is not empty
    if not url:
        return jsonify({'error': 'URL cannot be empty'})
    
    # Add http:// if not present
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    # Use ML prediction if available, otherwise fallback to rule-based
    try:
        # First try to use the ML model
        result = predict_url(url)
    except Exception as e:
        # Fallback to rule-based if ML fails
        print(f"ML prediction failed: {e}. Falling back to rule-based only.")
        # Extract features
        features = extract_features(url)
        # Calculate phishing score based on features
        suspicious_count = sum(1 for value in features.values() if value)
        total_features = len(features)
        # Determine if phishing
        is_phishing = suspicious_count >= 2
        confidence = min(suspicious_count / total_features * 100, 95)
        
        result = {
            'is_phishing': is_phishing,
            'confidence': confidence,
            'features': features,
            'method': 'rule-based only'
        }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)