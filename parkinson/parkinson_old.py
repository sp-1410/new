import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import joblib

df = pd.read_csv("parkinsons.csv")


print(f"📊 Dataset Statistics:")
print(f"Total Records: {df.shape[0]}")
print(f"Healthy Cases (0): {df[df['status'] == 0].shape[0]} ({(df['status'] == 0).mean() * 100:.2f}%)")
print(f"Parkinson’s Cases (1): {df[df['status'] == 1].shape[0]} ({(df['status'] == 1).mean() * 100:.2f}%)")

# Select relevant features
features = ['MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)', 'MDVP:Shimmer']
target = 'status'  # 1 = Parkinson's, 0 = Healthy

X = df[features]
y = df[target]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

joblib.dump((model, scaler), "parkinson_model.pkl")

print("\n✅ Model trained successfully!")

# Model Performance Metrics
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

print("\n📊 Model Performance Metrics:")
print(f"✅ Accuracy: {accuracy:.2f}")
print(f"✅ Precision: {precision:.2f}")
print(f"✅ Recall: {recall:.2f}")
print(f"✅ F1-Score: {f1:.2f}")
print("\nConfusion Matrix:")
print(conf_matrix)

print("\n🔍 Classification Report:")
print(classification_report(y_test, y_pred))

def predict_parkinsons():
    print("\n🧐 Enter your voice measurement data for Parkinson’s detection:")

    try:
        input_data = []
        for feature in features:
            value = float(input(f"Enter value for {feature}: "))
            input_data.append(value)

        
        model, scaler = joblib.load("parkinson_model.pkl")

 
        input_data = np.array(input_data).reshape(1, -1)
        input_data = scaler.transform(input_data)

        
        prediction = model.predict(input_data)[0]

        if prediction == 1:
            print("🚨 ALERT: You MAY have Parkinson’s disease. Please consult a doctor.")
        else:
            print("✅ You are unlikely to have Parkinson’s disease. Stay healthy!")
    
    except ValueError:
        print("⚠️ Invalid input! Please enter numeric values.")

predict_parkinsons()
