#include <ArduinoBLE.h>

const int buzzerPin = 5; // Pin for the buzzer

// Default values
String deviceName = "NFTag B";
float lat = -0.274294;
float lon = 36.069287;
String uuid = "b3d4f4c2-8b2b-4c1a-9d4b-8b92f0b1d97e";
String email = "DEFAULT_EMAIL";
float nftValue = 150.00;
String ownerContact = "+65 1234567433";
String customMessage = "I'm fun and track assets";
String owner = "John Doe";
String uniqueCode = "1234";
String status = "not connected";
String toggleStatus = "normal";

// BLE Characteristics
BLEService infoService("180D"); // Custom UUID for the information service
BLECharacteristic infoCharacteristic("2A37", BLERead | BLEWrite, 512); // Custom UUID for info

BLECharacteristic messageCharacteristic("2A38", BLERead | BLEWrite, 256); // Custom UUID for custom message
BLECharacteristic alarmCharacteristic("2A39", BLERead | BLEWrite, 4); // Custom UUID for alarm

void setup() {
  Serial.begin(115200);

  // Initialize BLE
  if (!BLE.begin()) {
    Serial.println("Starting BLE failed!");
    while (1);
  }
  
  BLE.setLocalName(deviceName);
  BLE.setAdvertisedService(infoService);

  // Add characteristics to the service
  infoService.addCharacteristic(infoCharacteristic);
  infoService.addCharacteristic(messageCharacteristic);
  infoService.addCharacteristic(alarmCharacteristic);
  
  // Add service
  BLE.addService(infoService);

  // Set initial values
  updateInfoCharacteristic();
  messageCharacteristic.setValue(customMessage);
  alarmCharacteristic.setValue(0); // No alarm initially

  // Start advertising
  BLE.advertise();
  Serial.println("BLE Advertise started");

  // Initialize Buzzer
  pinMode(buzzerPin, OUTPUT);
}

void loop() {
  BLEDevice central = BLE.central();
  
  if (central) {
    Serial.print("Connected to ");
    Serial.println(central.address());

    // Set status to connected
    status = "connected";

    while (central.connected()) {
      // Handle characteristic updates
      if (infoCharacteristic.written()) {
        String newInfo = infoCharacteristic.value().c_str();
        updateDeviceInfo(newInfo);
      }
      
      if (messageCharacteristic.written()) {
        customMessage = messageCharacteristic.value().c_str();
        Serial.println("Custom message updated: " + customMessage);
      }

      if (alarmCharacteristic.written()) {
        int frequency = alarmCharacteristic.value().toInt();
        if (frequency > 0) {
          playAlertSound(frequency);
        }
      }

      delay(100); // Small delay for stability
    }

    Serial.print("Disconnected from ");
    Serial.println(central.address());

    // Set status to disconnected
    status = "not connected";
  }
}

void updateDeviceInfo(String info) {
  // Parse and update device information
  // Example format: "lat:-0.123456,lon:36.654321"
  int latIndex = info.indexOf("lat:");
  int lonIndex = info.indexOf("lon:");
  if (latIndex != -1 && lonIndex != -1) {
    lat = info.substring(latIndex + 4, info.indexOf(',', latIndex)).toFloat();
    lon = info.substring(lonIndex + 4).toFloat();
  }
  // Update characteristic with new information
  updateInfoCharacteristic();
}

void updateInfoCharacteristic() {
  String message = "Name: " + deviceName + "\n";
  message += "Location: " + String(lat, 6) + ", " + String(lon, 6) + "\n";
  message += "Email: " + email + "\n";
  message += "NFT Value: $" + String(nftValue) + "\n";
  message += "Contact: " + ownerContact + "\n";
  message += "Owner: " + owner + "\n";
  message += "Code: " + uniqueCode + "\n";
  message += "Status: " + status + "\n";
  message += "Toggle: " + toggleStatus + "\n";
  message += "Custom Message: " + customMessage + "\n";

  infoCharacteristic.setValue(message);
}

void playAlertSound(int frequency) {
  tone(buzzerPin, frequency);
  delay(1000); // Sound duration
  noTone(buzzerPin);
}
