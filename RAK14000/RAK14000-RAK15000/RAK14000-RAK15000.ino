/**
   @file RAK14000-Epaper-Monochrome.ino.ino
   @author taylor.lee (taylor.lee@rakwireless.com)
   @brief display image and text on DEPG0213BNS800F42HP epaper,
          and control by botton
   @version 0.1
   @date 2021-02-18
   @copyright Copyright (c) 2021

*/

#include <Arduino.h>
#include <Adafruit_TinyUSB.h>
#include <qrcode.h>
// https://github.com/ricmoo/qrcode/

#include <Adafruit_GFX.h>
#include <Adafruit_EPD.h>
#include "images.h"
#include "Format.h"

char buffer[256];

QRCode qrcode;
uint8_t version = 3;

/**
   @brief Produces a QR Code, to be displayed on the EPD
          and on the Serial Monitor
*/
void showQRCode(char *msg) {
  display.clearBuffer();
  uint16_t sz = qrcode_getBufferSize(version);
  uint8_t qrcodeData[sz];
  qrcode_initText(&qrcode, qrcodeData, version, 0, msg);
  uint8_t myWidth = qrcode.size;
  uint16_t qrc_wd = myWidth / 2;
  if (myWidth * 2 != qrc_wd) qrc_wd += 1;
  uint16_t qrc_hg = myWidth * 4;
  uint16_t qrc_sz = qrc_wd * qrc_hg, ix = 0;
  unsigned char qrc[qrc_sz];
  // Text version: look at the Serial Monitor :-)
  Serial.print("\n\n\n\n");
  for (uint8_t y = 0; y < myWidth; y++) {
    // Left quiet zone
    Serial.print("        ");
    // Each horizontal module
    uint16_t px = ix;
    for (uint8_t x = 0; x < myWidth; x += 2) {
      // Print each module (UTF-8 \u2588 is a solid block)
      Serial.print(qrcode_getModule(&qrcode, x, y) ? "\u2588\u2588" : "  ");
      uint8_t c = 0;
      if (qrcode_getModule(&qrcode, x, y)) c = 0xF0;
      if (x + 1 < myWidth && qrcode_getModule(&qrcode, x + 1, y)) {
        c += 0x0F;
        Serial.print("\u2588\u2588");
      } else Serial.print("  ");
      qrc[ix++] = c;
    }
    memcpy(qrc + ix, qrc + px, qrc_wd);
    px = ix;
    ix += qrc_wd;
    memcpy(qrc + ix, qrc + px, qrc_wd);
    px = ix;
    ix += qrc_wd;
    memcpy(qrc + ix, qrc + px, qrc_wd);
    px = ix;
    ix += qrc_wd;
    Serial.print("\n");
  }
  // Bottom quiet zone
  Serial.print("\n\n\n\n");
  display.drawBitmap(0, 0, qrc, qrc_wd * 8, qrc_hg, EPD_BLACK);
  display.display(true);
}

void setup() {
  time_t timeout = millis();
  while (!Serial) {
    if ((millis() - timeout) < 5000) {
      delay(100);
    } else {
      break;
    }
  }
  Serial.begin(115200);
  delay(300);
  Serial.println("=====================================");
  Serial.println("        QR Code EPD LoRa Test");
  Serial.println("=====================================");
  Serial.println("          Turning on modules");
  pinMode(WB_IO2, INPUT_PULLUP); // EPD
  digitalWrite(WB_IO2, HIGH);
  delay(300);
  Serial.println("=====================================");
#ifdef _USE_EEPROM_
  if (i2ceeprom.begin(EEPROM_ADDR)) {
    // you can put a different I2C address here, e.g. begin(0x51);
    Serial.println("Found I2C EEPROM");
  } else {
    Serial.println("I2C EEPROM not identified ... check your connections?\r\n");
    while (1) {
      delay(10);
    }
  }
#ifdef _INITIALIZE_
  initEEPROM();
#endif
  readEEPROM();
#endif
  Serial.println("Epaper-QRCode test");
  display.begin();
  memset(buffer, 0, 256);
  uint8_t ln = strlen(myName);
  memcpy(buffer, myName, ln);
  buffer[ln++] = ':';
  buffer[ln++] = ' ';
  memcpy(buffer + ln, myText, strlen(myText));
  hexDump(buffer, strlen(buffer));
  showQRCode(buffer);
  display.drawBitmap(192, 0, rak_img, 150, 56, EPD_BLACK);
  testdrawtext(120, 60, myName, EPD_BLACK, 2);
  display.display(true);
}

void loop() {
}
