#include <BluetoothSerial.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>  // Include Adafruit ILI9341 library for the LCD screen

BluetoothSerial ESP_BT;
Adafruit_ILI9341 lcd = Adafruit_ILI9341(10, 9); // Adjust pins according to your setup

const int buzzerPin = 21; // Pin for the buzzer

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

// Buffer for image data
#define IMAGE_BUFFER_SIZE 1024
uint8_t imageBuffer[IMAGE_BUFFER_SIZE];

void setup() {
  Serial.begin(115200);
  Wire.begin();
  
  // Initialize Bluetooth
  ESP_BT.begin("NFTag_Bluetooth");
  Serial.println("Bluetooth Started");
  
  // Initialize LCD
  lcd.begin();
  lcd.setRotation(1);  // Landscape mode
  lcd.fillScreen(ILI9341_WHITE);

  // Initialize Buzzer
  pinMode(buzzerPin, OUTPUT);

  // Set up Bluetooth callback
  ESP_BT.register_callback(BluetoothCallback);
}

void loop() {
  // Keep checking for Bluetooth messages
  if (ESP_BT.available()) {
    String command = ESP_BT.readStringUntil('\n');
    processCommand(command);
  }

  // Optionally, broadcast information periodically
  broadcastInfo();
}

void BluetoothCallback(esp_spp_cb_event_t event, esp_spp_cb_param_t *param) {
  if (event == ESP_SPP_SRV_OPEN_EVT) {
    Serial.println("Bluetooth device connected");
    status = "connected";
  } else if (event == ESP_SPP_CLOSE_EVT) {
    Serial.println("Bluetooth device disconnected");
    status = "not connected";
  }
}

void processCommand(String command) {
  if (command.startsWith("UPDATE_INFO")) {
    // Update device information based on command
    String info = command.substring(11);
    updateDeviceInfo(info);
  } else if (command.startsWith("SEND_IMAGE")) {
    // Receive and store image data
    receiveImageData();
  } else if (command.startsWith("SET_MESSAGE")) {
    // Set custom message
    customMessage = command.substring(11);
    displayCustomMessage();
  } else if (command.startsWith("PLAY_ALERT")) {
    // Play alert sound
    int frequency = command.substring(11).toInt();
    playAlertSound(frequency);
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
  // Update display with new information
  displayDeviceInfo();
}

void displayDeviceInfo() {
  lcd.fillScreen(ILI9341_WHITE);
  lcd.setCursor(0, 0);
  lcd.setTextColor(ILI9341_BLACK);
  lcd.setTextSize(2);
  lcd.println("Name: " + deviceName);
  lcd.println("Location: " + String(lat, 6) + ", " + String(lon, 6));
  lcd.println("Email: " + email);
  lcd.println("NFT Value: $" + String(nftValue));
  lcd.println("Contact: " + ownerContact);
  lcd.println("Owner: " + owner);
  lcd.println("Code: " + uniqueCode);
  lcd.println("Status: " + status);
  lcd.println("Toggle: " + toggleStatus);
}

void receiveImageData() {
  // Simulate receiving image data
  // Example: Fill buffer with some dummy data
  for (int i = 0; i < IMAGE_BUFFER_SIZE; i++) {
    imageBuffer[i] = i % 256;
  }
  // Display image (This is just an example; you need actual image handling)
  lcd.fillScreen(ILI9341_BLACK);
  lcd.drawRect(10, 10, 100, 100, ILI9341_RED);
}

void displayCustomMessage() {
  lcd.fillScreen(ILI9341_WHITE);
  lcd.setCursor(0, 0);
  lcd.setTextColor(ILI9341_BLACK);
  lcd.setTextSize(2);
  lcd.println(customMessage);
}

void playAlertSound(int frequency) {
  // Simple buzzer sound function
  tone(buzzerPin, frequency);
  delay(1000); // Sound duration
  noTone(buzzerPin);
}

void broadcastInfo() {
  if (status == "connected") {
    // Construct the broadcast message
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
    
    // Send the message via Bluetooth
    ESP_BT.println(message);
    Serial.println("Broadcasting info: " + message);

    // Optional: Add a delay between broadcasts
    delay(10000); // Broadcast every 10 seconds
  }
}
