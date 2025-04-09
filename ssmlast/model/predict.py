import pickle
import os
import re
from urllib.parse import urlparse

# Function to extract features from a URL using rule-based methods
def extract_features(url):
    features = {}
    
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Check for suspicious TLDs
    suspicious_tlds = ['.xyz', '.top', '.club', '.online', '.live', '.site', '.info', '.tech']
    features['suspicious_tld'] = any(parsed_url.netloc.endswith(tld) for tld in suspicious_tlds)
    
    # Check for numbers in domain
    features['numbers_in_domain'] = bool(re.search(r'\d', parsed_url.netloc))
    
    # Check for suspicious keywords
    suspicious_keywords = ['secure', 'account', 'banking', 'login', 'verify', 'update', 'confirm', 
                          'signin', 'security', 'authenticate', 'wallet', 'password','fake']
    features['suspicious_keywords'] = any(keyword in url.lower() for keyword in suspicious_keywords)
    
    # Check for excessive subdomains
    subdomain_count = len(parsed_url.netloc.split('.')) - 2
    features['excessive_subdomains'] = subdomain_count > 2
    
    # URL length (phishing URLs tend to be longer)
    features['long_url'] = len(url) > 75
    
    # Check for IP address in URL
    features['ip_in_url'] = bool(re.match(r'\d+\.\d+\.\d+\.\d+', parsed_url.netloc))
    
    # Check for URL shortening services
    shortening_services = ['bit.ly', 'goo.gl', 'tinyurl', 't.co', 'is.gd', 'cli.gs', 'ow.ly']
    features['shortened_url'] = any(service in parsed_url.netloc for service in shortening_services)
    
    return features

# Load the trained model and vectorizer
def load_model():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, 'phishing_model.pkl')
    vectorizer_path = os.path.join(script_dir, 'vectorizer.pkl')
    
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
        
        return model, vectorizer
    except FileNotFoundError:
        return None, None

# Predict if a URL is phishing
def predict_url(url):
    model, vectorizer = load_model()
    
    # Extract rule-based features
    features = extract_features(url)
    
    if model is None or vectorizer is None:
        # If model doesn't exist, use rule-based detection only
        suspicious_score = sum(1 for value in features.values() if value)
        is_phishing = suspicious_score >= 2
        confidence = min(suspicious_score / len(features) * 100, 95)
        
        return {
            'is_phishing': is_phishing,
            'confidence': confidence,
            'features': features,
            'method': 'rule-based'
        }
    
    # Use both ML model and rule-based approach
    # Vectorize the URL
    url_vec = vectorizer.transform([url])
    
    # Get model prediction and probability
    is_phishing = bool(model.predict(url_vec)[0])
    probability = model.predict_proba(url_vec)[0][1] * 100  # Probability of being phishing
    
    # Combine ML prediction with rule-based features
    rule_based_score = sum(1 for value in features.values() if value) / len(features)
    
    # Calculate combined confidence
    confidence = probability * 0.7 + (rule_based_score * 100) * 0.3
    
    return {
        'is_phishing': is_phishing,
        'confidence': confidence,
        'features': features,
        'method': 'machine learning + rule-based'
    }
