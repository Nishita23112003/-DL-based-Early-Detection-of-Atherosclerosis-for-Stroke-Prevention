#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"
#include <SoftwareSerial.h>

MAX30105 particleSensor;

#define GSR_PIN A1
#define ECG_PIN A0
const float fixedResistor = 10000.0;  // 10kΩ pull-down resistor for GSR

SoftwareSerial bpSerial(2, 3);  // RX, TX for BP sensor
int sysBP = 0, diaBP = 0, heartRate = 0;
float spo2 = -1.0;  // Default invalid value

void setup() {
    Serial.begin(115200);
    bpSerial.begin(9600);

    if (!particleSensor.begin(Wire, I2C_SPEED_STANDARD)) {
        Serial.println("MAX30102 not found!");
        while (1);
    }
    particleSensor.setup();
}

void loop() {
    // Read PPG Sensor
    long irValue = particleSensor.getIR();
    long redValue = particleSensor.getRed();
    
    if (irValue > 50000 && redValue > 50000) {  // Ensure signal strength is strong
        checkForBeat(irValue);
        int validHeartRate = particleSensor.getIR() / 1000; // Approximate HR
        if (validHeartRate > 40 && validHeartRate < 180) {
            heartRate = validHeartRate;
        }

        // Compute SpO2 using red/IR ratio
        float ratio = (float)redValue / (float)irValue;
        spo2 = 110 - (ratio * 25);
        spo2 = constrain(spo2, 80, 100); // Ensure realistic SpO2 values
    }

    // Read ECG Signal
    int ecgValue = analogRead(ECG_PIN);

    // Read GSR Sensor
    int gsrValue = analogRead(GSR_PIN);
    float gsrResistance = (gsrValue == 0) ? 0 : ((1023.0 - gsrValue) * fixedResistor) / gsrValue;  // Avoid division by zero

    // Read BP Sensor Data
    if (bpSerial.available()) {
        String bpData = bpSerial.readStringUntil('\\n');  // Read BP data line
        int firstComma = bpData.indexOf(',');
        int secondComma = bpData.indexOf(',', firstComma + 1);
        int thirdComma = bpData.indexOf(',', secondComma + 1);

        if (firstComma != -1 && secondComma != -1 && thirdComma != -1) {
            sysBP = bpData.substring(firstComma + 1, secondComma).toInt();
            diaBP = bpData.substring(secondComma + 1, thirdComma).toInt();
            int receivedHR = bpData.substring(thirdComma + 1).toInt();
            if (receivedHR > 40 && receivedHR < 180) { // Ignore unrealistic HR values
                heartRate = receivedHR;
            }
        }
    }

    // Send Packet Format: H<HR> S<SpO2> G<GSR> E<ECG> L<Systolic> D<Diastolic>
    Serial.print("H"); Serial.print(heartRate);
    Serial.print(" S"); Serial.print(spo2, 1);  // Print with one decimal place
    Serial.print(" G"); Serial.print(gsrResistance / 1000, 2); // Convert to kΩ, two decimal places
    Serial.print(" E"); Serial.print(ecgValue);
    Serial.print(" L"); Serial.print(sysBP);
    Serial.print(" D"); Serial.println(diaBP);

    delay(500);
}