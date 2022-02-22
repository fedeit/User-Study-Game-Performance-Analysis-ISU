#include <BleKeyboard.h>
#include <string.h>
#include <BleMouse.h>
#include <math.h>

BleMouse bleMouse;
//BleKeyboard bleKeyboard;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  bleMouse.begin();
//  bleKeyboard.begin();
}

void move(int x, int y) {
  int sx = 1, sy = 1;
  if (x < 0) sx = -1;
  if (y < 0) sy = -1;
  int i = 0;
  while (x != 0) {
    i++;
    int dx = 0;
    if (x != 0) dx = min(127, abs(x));
    x -= (sx * dx);
    signed char p = sx*dx;
    bleMouse.move(p, 0, 0);
  }
  i=0;
  while (y != 0) {
    i++;
    int dy = 0;
    if (y != 0) dy = min(127, abs(y));
    y -= (sy * dy);
    signed char p = sy*dy;
    bleMouse.move(0, p, 0);
  }
  
//  while (x != 0 || y != 0) {
//    int dx = 0, dy = 0;
//    if (x != 0) dx = min(127, abs(x));
//    if (y != 0) dy = min(127, abs(y));
//    bleMouse.move(sx * dx, sy * dy, 0);  
//    x -= (sx * dx);
//    y -= (sy * dy);
//  }
}


void loop() {
  while (!Serial.available());
  String str = Serial.readString();
  char * pch = strtok((char *)str.c_str(), ",");
  int pIDX = 0;
  int action = -1;
  int p1 = -1;
  int p2 = -1;
  int p3 = -1;
  while (pch != NULL) {
    pIDX++;
    switch(pIDX) {
      case 1: action = atoi(pch); break;
      case 2: p1 = atoi(pch); break;
      case 3: p2 = atoi(pch); break;
      case 4: p3 = atoi(pch); break;
    }
    pch = strtok(NULL, ",");
  }
  Serial.println(String(action)+", "+String(p1)+", "+String(p2)+", "+String(p3));

  if(bleMouse.isConnected()) {
    switch(action) {
      case 1: // click
      move(p1, p2);
      delay(500);
      bleMouse.click();
      break;

      case 2: // moveTo
      //bleMouse.click(xReading, yReading, 0);
      move(p1, p2);
      break;

      case 3: // doubleClick
      //MouseTo.mouse(p1, p2);
      move(p1, p2);
      delay(500);
      bleMouse.click();
      //bleMouse.click();
      delay(250);
      bleMouse.click();
      //bleMouse.click();
      break;

//      case 4: // keydown
//          bleKeyboard.press(p3);
//      break;
//
//      case 5:  // keyup
//          bleKeyboard.release(p3);
//      break;
//
//      case 6: // press
//          bleKeyboard.write(p3);
//      break;
      
    }
   Serial.println("0");
  } else {
      Serial.println("Waitig BLE!");
      Serial.println("1");
  }
}