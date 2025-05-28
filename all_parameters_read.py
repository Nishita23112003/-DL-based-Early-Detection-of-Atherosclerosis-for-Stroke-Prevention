import serial
import re
import csv
import time

# Open Serial Port
ser = serial.Serial('COM3', 115200, timeout=1)  # Change 'COM3' if needed

data_list = []
num_readings = 50  # Number of readings to collect

timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")  # Unique timestamp for the file
csv_filename = f"sensor_data_{timestamp}.csv"

# ✅ Open CSV File with UTF-8 Encoding
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Heart Rate (bpm)", "SpO2 (%)", "GSR (kΩ)", "ECG", "Systolic BP (mmHg)", "Diastolic BP (mmHg)"])

    print("Collecting data... Press Ctrl+C to stop early.")
    count = 0

    # ✅ Store last valid BP values
    last_sys_bp = None
    last_dia_bp = None

    while count < num_readings:
        try:
            line = ser.readline().decode('utf-8').strip()
            
            # Extract values using regex
            match = re.search(r'H(\d+)\s+S([\d.]+)\s+G([\d.]+)\s+E(\d+)\s+L(\d+)\s+D(\d+)', line)
            if match:
                heart_rate = int(match.group(1))
                spo2 = float(match.group(2))
                gsr = float(match.group(3))
                ecg = int(match.group(4))
                sys_bp = int(match.group(5))
                dia_bp = int(match.group(6))

                # ✅ Ignore BP sensor values if they are 0 (invalid readings)
                if sys_bp == 0 or dia_bp == 0:
                    print("⚠ BP sensor not measured yet, using last valid values.")
                    sys_bp = last_sys_bp if last_sys_bp is not None else "N/A"
                    dia_bp = last_dia_bp if last_dia_bp is not None else "N/A"
                else:
                    last_sys_bp = sys_bp
                    last_dia_bp = dia_bp

                # Save to CSV
                writer.writerow([heart_rate, spo2, gsr, ecg, sys_bp, dia_bp])
                
                # Print Data
                print(f"Reading {count+1}/{num_readings}")
                print(f"Heart Rate: {heart_rate} bpm")
                print(f"SpO2: {spo2}%")
                print(f"GSR: {gsr} kΩ")
                print(f"ECG: {ecg}")
                print(f"BP: {sys_bp}/{dia_bp} mmHg")
                print("-" * 40)
                
                count += 1
        
        except KeyboardInterrupt:
            print("Stopping...")
            break

print(f"Data saved in {csv_filename}")
ser.close()