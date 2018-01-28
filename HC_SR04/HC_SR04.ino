/**
 * @author Harald Moritz
 * The main file for the HC_SR04s.
 */
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

/**
 * Sets up the Serial connection.
 */
void setup() {
  Serial.begin(9600);
}

/**
 * Compares two char array for equality.
 * 
 * @param str1 The first char array.
 * @param str2 The second char array.
 */
boolean equals(char* str1, char* str2) {
  return strncmp(str1, str2, strlen(str2)) == 0;
}

/**
 * The main loop to responde to the serial getters.
 */
void loop() {
  memset(&serIn, 0, sizeof(serIn));
  memset(&distances, 0, sizeof(distances));
  while (! Serial.available()) { }
  read(serIn);
  write(serIn);
  //Serial.println("Init");
  if (equals(serIn,  ">getDistances")) {
    if (us.getDistances(distances)) {
      sprintf(serOut, "<distances:%s,%s,%s,%s",
              dtostrf(distances[0], width, prec, double_str0),
              dtostrf(distances[1], width, prec, double_str1),
              dtostrf(distances[2], width, prec, double_str2),
              dtostrf(distances[3], width, prec, double_str3)
             );
    } else {
      sprintf(serOut, "<distances:null");
    }
  } else if (equals(serIn, ">getFront")) {
    sprintf(serOut, "<front:%s", dtostrf(us.measureOne(6, 2), width, prec, double_str0));
  } else {
    sprintf(serOut, "<null");
  }
    write(serOut);
}

/**
 * Puts the  output on the Serial connection.
 * 
 * @param buff A char array to write to the Serial connection.
 */
void write(char* buff) {
  Serial.println(buff);
}

/**
 * Reads from the Serial connection to the buffer.
 * 
 * @param buff The char array buffer to write to.
 */
void read(char* buff) {
  int index = 0;
  while (Serial.available()) {
    buff[index] = Serial.read();
    index ++;
    delay(10);
  }
}

