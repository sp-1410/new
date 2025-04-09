import pandas as pd
import numpy as np
import pickle
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# Function to create a sample dataset of legitimate and phishing URLs
def create_sample_dataset():
    # Legitimate URLs
    legitimate_urls = [
        "google.com", "youtube.com", "facebook.com", "wikipedia.org", "amazon.com",
        "twitter.com", "instagram.com", "linkedin.com", "microsoft.com", "apple.com",
        "netflix.com", "github.com", "reddit.com", "nytimes.com", "cnn.com",
        "yahoo.com", "ebay.com", "paypal.com", "tumblr.com", "pinterest.com",
        "dropbox.com", "adobe.com", "spotify.com", "wordpress.com", "imgur.com"
    ]
    
    # Phishing URLs (examples with common phishing patterns)
    phishing_urls = [
        "g00gle.com", "facebo0k.com", "secure-login-paypal.com", "verify-account-apple.com",
        "m1crosoft-update.com", "signin-update-amazon.com", "account-verify-netflix.com",
        "verify-banking-login.com", "secure-payment-confirm.club", "account-update-service.xyz",
        "validate-your-account.site", "security-alert-verify.online", "banking-secure-login.top",
        "facebook-security-check.xyz", "apple-id-verify-now.com", "secure-bank-login.live",
        "verification-required-paypal.com", "google-secure-signin.club", "amazon-account-verify.site",
        "login-secure-verification.online", "account-update-required.xyz", "banking-alert-verify.top",
        "microsoft-account-security.club", "netflix-update-billing.com", "verification-center-paypal.site"
        "fake.com","clickme-real.com","http://free-giftcards123.com"
    ]
    
    # Create DataFrame with URLs and labels
    urls = legitimate_urls + phishing_urls
    labels = [0] * len(legitimate_urls) + [1] * len(phishing_urls)  # 0 for legitimate, 1 for phishing
    
    return pd.DataFrame({'url': urls, 'is_phishing': labels})

# Function to train and save the model
def train_model():
    print("Starting model training...")
    
    # Create or use dataset
    try:
        # Try to load existing dataset if available
        df = pd.read_csv('model/phishing_dataset.csv')
        print(f"Loaded existing dataset with {len(df)} URLs")
    except:
        # Create sample dataset if no dataset exists
        df = create_sample_dataset()
        os.makedirs('model', exist_ok=True)
        df.to_csv('model/phishing_dataset.csv', index=False)
        print(f"Created sample dataset with {len(df)} URLs")
    
    # Feature extraction - convert URLs to feature vectors
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df['url'])
    y = df['is_phishing']
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Naive Bayes model
    model = MultinomialNB()
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    print(f"Model Accuracy: {accuracy:.2f}")
    print(f"Classification Report:\n{report}")
    
    # Save model and vectorizer
    os.makedirs('model', exist_ok=True)
    with open('model/phishing_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('model/vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    
    print("Model and vectorizer saved successfully")
    return model, vectorizer

if __name__ == "__main__":
    train_model()