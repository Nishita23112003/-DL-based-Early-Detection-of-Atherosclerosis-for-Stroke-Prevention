import serial
import csv
import time

# Generate a timestamped filename
timestamp = time.strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
csv_filename = f"ecg_data_{timestamp}.csv"

# Replace 'COM3' with your actual Arduino port
ser = serial.Serial('COM3', 115200, timeout=1)  # Match baud rate with Arduino
time.sleep(2)  # Wait for connection to establish

try:
    with open(csv_filename, "w", newline="") as file:  # Open new CSV file
        writer = csv.writer(file)
        writer.writerow(["Heart Rate", "HRV", "ECG Value"])  # CSV Header
        
        print(f"Collecting 50 ECG readings... Data will be saved in: {csv_filename}")
        reading_count = 0
        
        while reading_count < 50:  # Collect exactly 50 readings
            line = ser.readline().decode('utf-8').strip()  # Read data from Serial
            data = line.split(',')

            if len(data) == 3:  # Ensure valid data format
                writer.writerow(data)
                print(f"Reading {reading_count+1}: {data}")  # Print the saved data
                reading_count += 1
                time.sleep(1)  # *Wait 1 second before next reading*

except Exception as e:
    print(f"Error: {e}")

finally:
    ser.close()
    print(f"\nData collection complete. ECG data saved in '{csv_filename}'.")