#include <WiFi.h>
#include <WebServer.h>
#include <esp32cam.h>
#include <ArduinoOTA.h>  // Include OTA library

// WiFi credentials
const char* WIFI_SSID = "";         
const char* WIFI_PASS = "";      

WebServer server(80);  // HTTP server on port 80

// Camera resolutions
static auto hiRes = esp32cam::Resolution::find(800, 600);

void setup() {
  Serial.begin(115200);
  Serial.println();

  {
    using namespace esp32cam;
    Config cfg;
    cfg.setPins(pins::AiThinker);
    cfg.setResolution(hiRes);  // Set the initial resolution
    cfg.setBufferCount(2);
    cfg.setJpeg(80);

    bool ok = Camera.begin(cfg);
    Serial.println(ok ? "CAMERA OK" : "CAMERA FAIL");
    if (!ok) {
      ESP.restart();  // Restart ESP32 if the camera initialization fails
    }
  }

  // Connect to WiFi
  WiFi.persistent(false);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  // Wait for the WiFi connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.print("Connected to WiFi. IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.println("Access camera streams:");
  Serial.println("  /cam-hi.jpg");

  ArduinoOTA.onStart([]() {
    String type;
    if (ArduinoOTA.getCommand() == U_FLASH) {
      type = "sketch";
    } else { // U_SPIFFS
      type = "filesystem";
    }
    Serial.println("Start updating " + type);
  });

  ArduinoOTA.onEnd([]() {
    Serial.println("\nEnd");
  });

  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
    Serial.printf("Progress: %u%%\r", (progress / (total / 100)));
  });

  ArduinoOTA.onError([](ota_error_t error) {
    Serial.printf("Error[%u]: ", error);
    if (error == OTA_AUTH_ERROR) {
      Serial.println("Auth Failed");
    } else if (error == OTA_BEGIN_ERROR) {
      Serial.println("Begin Failed");
    } else if (error == OTA_CONNECT_ERROR) {
      Serial.println("Connect Failed");
    } else if (error == OTA_RECEIVE_ERROR) {
      Serial.println("Receive Failed");
    } else if (error == OTA_END_ERROR) {
      Serial.println("End Failed");
    }
  });

  ArduinoOTA.begin();

  // Set up HTTP server routes for camera streams
  server.on("/cam-lo.jpg", []() {
    if (!esp32cam::Camera.changeResolution(loRes)) {
      Serial.println("SET-LO-RES FAIL");
    }
    serveJpg();
  });

  server.on("/cam-hi.jpg", []() {
    if (!esp32cam::Camera.changeResolution(hiRes)) {
      Serial.println("SET-HI-RES FAIL");
    }
    serveJpg();
  });

  server.on("/cam-mid.jpg", []() {
    if (!esp32cam::Camera.changeResolution(midRes)) {
      Serial.println("SET-MID-RES FAIL");
    }
    serveJpg();
  });

  server.begin();  // Start the HTTP server
}

void loop() {
  server.handleClient();  // Handle HTTP server events
  ArduinoOTA.handle();    // Handle OTA updates
}

// Function to serve a JPEG image from the camera
void serveJpg() {
  auto frame = esp32cam::capture();
  if (frame == nullptr) {
    Serial.println("CAPTURE FAIL");
    server.send(503, "", "");
    return;
  }
  
  Serial.printf("CAPTURE OK %dx%d %db\n", frame->getWidth(), frame->getHeight(), static_cast<int>(frame->size()));

  server.setContentLength(frame->size());
  server.send(200, "image/jpeg");
  WiFiClient client = server.client();
  frame->writeTo(client);
}
