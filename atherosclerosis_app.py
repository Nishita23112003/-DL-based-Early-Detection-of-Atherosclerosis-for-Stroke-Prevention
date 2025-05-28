import streamlit as st
import numpy as np
import pandas as pd
import joblib
from tensorflow.keras.models import load_model

# ------------------- Load Model and Scaler -------------------
model = load_model("CNN-LSTM_best_model.h5",compile=False)  # Your trained CNN-LSTM model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

scaler = joblib.load("scaler.pkl")  # Your saved MinMaxScaler

# ------------------- Feature Extraction Function -------------------
def extract_features(df):
    df = df.copy()
    df["Pulse_Pressure"] = df["Systolic BP (mmHg)"] - df["Diastolic BP (mmHg)"]
    df["MAP"] = df["Diastolic BP (mmHg)"] + (df["Pulse_Pressure"] / 3)
    df["LDL_to_HDL"] = df["LDL"] / (df["HDL"] + 1e-6)
    df["Cholesterol_Ratio"] = df["Cholesterol"] / (df["HDL"] + 1e-6)
    df["HR_SpO2_Ratio"] = df["Heart Rate"] / (df["SpO2"] + 1e-6)
    return df

# ------------------- Streamlit UI -------------------
st.title('🫀 Atherosclerosis Detection Prediction')
st.write("This app evaluates your risk for atherosclerosis based on clinical and sensor data.")

# User inputs
age = st.number_input('Age', 1, 100, 50)
gender = st.selectbox('Gender', options=['Male', 'Female'], index=0)
gender = 0 if gender == 'Male' else 1

glucose = st.number_input('Glucose (mg/dL)', 50, 500, 100)
cholesterol = st.number_input('Cholesterol (mg/dL)', 50, 500, 180)
ldl = st.number_input('LDL (mg/dL)', 50, 500, 90)
hdl = st.number_input('HDL (mg/dL)', 20, 100, 55)
gsr = st.number_input('GSR (kΩ)', 1.0, 500.0, 75.0)
systolic = st.number_input('Systolic BP (mmHg)', 50, 200, 120)
diastolic = st.number_input('Diastolic BP (mmHg)', 30, 150, 80)
spo2 = st.number_input('SpO2 (%)', 50, 100, 98)
heart_rate = st.number_input('Heart Rate (bpm)', 40, 200, 75)
hrv = st.number_input('HRV (ms)', 0.5, 3.0, 1.2, step=0.1)
ecg = st.number_input('ECG Signal (bpm)', 30, 200, 75)

# ------------------- Prediction Button -------------------
if st.button("Predict Atherosclerosis"):

    # Step 1: Prepare Input Data
    input_data = pd.DataFrame([[
        age, gender, glucose, cholesterol, ldl, hdl, gsr, systolic,
        diastolic, spo2, heart_rate, hrv, ecg
    ]], columns=[
        "Age", "Gender", "Glucose", "Cholesterol", "LDL", "HDL", "GSR",
        "Systolic BP (mmHg)", "Diastolic BP (mmHg)", "SpO2", "Heart Rate",
        "HRV", "ECG"
    ])

    # Step 2: Feature Extraction
    input_features = extract_features(input_data)

    # Step 3: Reorder columns as per model training
    try:
        feature_columns = scaler.feature_names_in_
    except AttributeError:
        st.error("Scaler does not have feature_names_in_ attribute. Please ensure you saved it with `set_output(transform='pandas')` or use explicit column list.")
        st.stop()

    input_features = input_features[feature_columns]

    # Step 4: Normalize and reshape
    input_scaled = scaler.transform(input_features)
    input_reshaped = input_scaled.reshape(1, input_scaled.shape[1], 1)  # Shape for CNN-LSTM

    # Step 5: Predict
    prediction = model.predict(input_reshaped)[0][0]
    predicted_label = "Unhealthy (At Risk)" if prediction > 0.5 else "Healthy"

    # Step 6: Display
    st.subheader(f"Prediction: {predicted_label}")
    st.write(f"🔍 Model confidence: **{prediction:.2f}**")

        # Define normal range check logic
    risky_count = 0
    total_features = 11

    # Conditions
    if glucose < 70 or glucose > 140:
        risky_count += 1
    if cholesterol < 70 or cholesterol > 200:
        risky_count += 1
    if ldl > 100:
        risky_count += 1
    if hdl < 60:
        risky_count += 1
    if gsr < 50 or gsr > 100:
        risky_count += 1
    if systolic < 90 or systolic > 120:
        risky_count += 1
    if diastolic < 60 or diastolic > 80:
        risky_count += 1
    if spo2 < 95:
        risky_count += 1
    if heart_rate < 60 or heart_rate > 100:
        risky_count += 1
    if hrv < 0.8 or hrv > 2.0:
        risky_count += 1
    if ecg < 60 or ecg > 100:
        risky_count += 1
    if risky_count >= total_features / 2:
        st.error(f"🩺 {risky_count} out of {total_features} parameters are out of the healthy range.")
    else:
        st.success(f" Only {risky_count} out of {total_features} parameters are risky.")




    
	