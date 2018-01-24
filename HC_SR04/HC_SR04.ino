#include "HC_SR04.h"

HC_SR04 us;
char serIn[100];
char serOut[100];
double distances[4];

char double_str0[13];
char double_str1[13];
char double_str2[13];
char double_str3[13];
unsigned char width = 12;
unsigned char prec = 5;

void setup() {
  Serial.begin(9600);
}

boolean equals(char* str1, char* str2) {
  return strncmp(str1, str2, strlen(str2)) == 0;
}

void loop() {
  memset(&serIn, 0, sizeof(serIn));
  memset(&distances, 0, sizeof(distances));
  while (Serial.available()) { }
  read(serIn);
  if (equals(serIn,  ">getDistances")) {
    if (us.getDistances(distances)) {
      sprintf(serOut, "<distances:%s,%s,%s",
              dtostrf(distances[0], width, prec, double_str0),
              dtostrf(distances[1], width, prec, double_str1),
              dtostrf(distances[2], width, prec, double_str2),
              dtostrf(distances[3], width, prec, double_str3)
             );
    } else {
      sprintf(serOut, "<distances:null");
    }
  } else {
    sprintf(serOut, "<null");
  }
    write(serOut);
}

void write(char* buff) {
  Serial.println(buff);
}

void read(char* buff) {
  int index = 0;
  while (Serial.available()) {
    buff[index] = Serial.read();
    index ++;
    delay(10);
  }
}

