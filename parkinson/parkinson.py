import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("parkinsons.csv")

# Check column names
print("Dataset Columns:", df.columns)

# Select relevant features (fewer inputs)
features = ['MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)', 'MDVP:Shimmer']
target = 'status'  # 1 = Parkinson's, 0 = Healthy

# Extract feature data and labels
X = df[features]
y = df[target]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model
joblib.dump((model, scaler), "parkinson_model.pkl")

print("Model trained successfully!")

# Function to predict Parkinson’s
def predict_parkinsons():
    print("\n🧐 Enter your voice measurement data for Parkinson’s detection:")

    try:
        input_data = []
        for feature in features:
            value = float(input(f"Enter value for {feature}: "))
            input_data.append(value)

        # Load model
        model, scaler = joblib.load("parkinson_model.pkl")

        # Process input
        input_data = np.array(input_data).reshape(1, -1)
        input_data = scaler.transform(input_data)

        # Make prediction
        prediction = model.predict(input_data)[0]

        if prediction == 1:
            print("🚨 ALERT: You MAY have Parkinson’s disease. Please consult a doctor.")
        else:
            print("✅ You are unlikely to have Parkinson’s disease. Stay healthy!")
    
    except ValueError:
        print("⚠️ Invalid input! Please enter numeric values.")

# Run prediction function
predict_parkinsons()
