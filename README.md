# -DL-based-Early-Detection-of-Atherosclerosis-for-Stroke-Prevention
# DL-based Early Detection of Atherosclerosis for Stroke Prevention

This project aims to enable **early detection of atherosclerosis** using deep learning techniques on physiological signals. It helps in predicting the risk of stroke and allows timely preventive action.

---

## 📁 Folder Structure

- `data/`  
  Contains two CSV datasets:
  - `healthy_dataset.csv`
  - `unhealthy_dataset.csv`

- `arduino/`  
  Arduino and Python scripts used to collect real-time sensor data:
  - `ecg.ino`: Collects ECG signals
  - `four_parameters.ino`: Collects ECG, PPG, GSR, BP
  - `all_parameters_read.py`: Reads all data and saves to CSV
  - `ecg_read.py`: Reads ECG data and saves to CSV

- `streamlit/`  
  Contains the user interface:
  - `atherosclerosis_app.py`: A Streamlit app to collect 14 inputs and run the prediction

- `models/`  
  Pre-trained models and preprocessing tools:
  - `CNN-LSTM_best_model.h5`: Trained Deep Learning model
  - `scaler.pkl`: Scaler for input normalization

---

## 🧠 Features

- Collects real-time data using sensors (ECG, PPG, GSR, BP)
- Uses a CNN-LSTM hybrid model for prediction
- Web-based interface using Streamlit for entering inputs
- Predicts whether the patient is **healthy** or **at risk** of atherosclerosis

---

## 🚀 How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/DL-atherosclerosis-detection.git
   cd DL-atherosclerosis-detection
