import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import streamlit as st

# --- Data Load ---
df = pd.read_csv('Sleep_health_and_lifestyle_dataset.csv')
print("Dataset shape:", df.shape)
print(df.head())

# --- Data Preprocessing ---
# Fill missing Sleep Disorder values with None
df['Sleep Disorder'] = df['Sleep Disorder'].fillna('None')

# Drop Person ID
df = df.drop('Person ID', axis=1)

# Split Blood Pressure into SystolicBP and DiastolicBP
bp_split = df['Blood Pressure'].str.split('/', expand=True).astype(int)
df['SystolicBP'], df['DiastolicBP'] = bp_split[0], bp_split[1]
df = df.drop('Blood Pressure', axis=1)

print(df.info())

# --- Encode Categorical Variables ---
categorical_cols = ['Gender', 'Occupation', 'BMI Category', 'Sleep Disorder']
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le
    print(f"{col} classes: {le.classes_}")

print(df.head())

# --- Train-Test Split ---
X = df.drop('Sleep Disorder', axis=1)
y = df['Sleep Disorder']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print("Training set size:", X_train.shape)
print("Test set size:", X_test.shape)

# --- Train Decision Tree Model ---
model = DecisionTreeClassifier(max_depth=5, min_samples_split=2, min_samples_leaf=2, random_state=42)
model.fit(X_train, y_train)
print("Model trained successfully!")

# --- Model Evaluation ---
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy*100:.2f}%")
print("Classification Report:\n", classification_report(y_test, y_pred, target_names=label_encoders['Sleep Disorder'].classes_))

# --- Save model and encoders ---
model_data = {
    'model': model,
    'label_encoders': label_encoders,
    'feature_names': list(X.columns)
}
joblib.dump(model_data, 'sleepdisordermodel.pkl')
print("Model saved successfully as sleepdisordermodel.pkl")

# --- Streamlit App ---

st.set_page_config(page_title="Sleep Disorder Predictor", page_icon="😴")

def encode_input(inputs, label_encoders):
    # Replace "" with default 'unknown' encoding: here 0 for simplicity
    for col, le in label_encoders.items():
        if col in inputs:
            val = inputs[col]
            if val == "" or val not in le.classes_:
                inputs[col] = 0
            else:
                inputs[col] = le.transform([val])[0]
    return inputs

def sleep_disorder_prediction_ui():
    st.title("Sleep Disorder Prediction")

    gender = st.selectbox("Gender", ["Select Gender"] + list(label_encoders['Gender'].classes_), index=0)
    age = st.slider("Age", 10, 100, 30)
    occupation = st.selectbox("Occupation", ["Select Occupation"] + list(label_encoders['Occupation'].classes_), index=0)
    sleep_duration = st.slider("Sleep Duration (hours)", 0.0, 12.0, 7.0, step=0.1)
    quality_of_sleep = st.slider("Quality of Sleep (1-10)", 1, 10, 5)
    physical_activity_level = st.slider("Physical Activity Level (1-10)", 1, 10, 5)
    stress_level = st.slider("Stress Level (1-10)", 1, 10, 5)
    bmi_category = st.selectbox("BMI Category", ["Select BMI Category"] + list(label_encoders['BMI Category'].classes_), index=0)
    heart_rate = st.slider("Heart Rate (bpm)", 40, 150, 75)
    daily_steps = st.slider("Daily Steps", 0, 20000, 5000, step=100)
    systolic_bp = st.slider("Systolic Blood Pressure (mmHg)", 90, 180, 120)
    diastolic_bp = st.slider("Diastolic Blood Pressure (mmHg)", 60, 120, 80)

    user_inputs = {
        "Gender": gender,
        "Age": age,
        "Occupation": occupation,
        "Sleep Duration": sleep_duration,
        "Quality of Sleep": quality_of_sleep,
        "Physical Activity Level": physical_activity_level,
        "Stress Level": stress_level,
        "BMI Category": bmi_category,
        "Heart Rate": heart_rate,
        "Daily Steps": daily_steps,
        "SystolicBP": systolic_bp,
        "DiastolicBP": diastolic_bp
    }

    encoded_inputs = encode_input(user_inputs.copy(), label_encoders)

    input_df = pd.DataFrame([encoded_inputs], columns=model_data['feature_names'])

    if st.button("Predict Sleep Disorder"):
        prediction = model.predict(input_df)[0]
        pred_label = label_encoders['Sleep Disorder'].inverse_transform([prediction])[0]
        st.success(f"Predicted Sleep Disorder: {pred_label}")

if __name__ == "__main__":
    sleep_disorder_prediction_ui()
