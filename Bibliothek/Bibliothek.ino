/**
 * A Arduino file to control the I2C Arduino.
 */
#include <Wire.h>

#include <FastLED.h>
#include <Servo.h>
//#include <SparkFun_APDS9960.h>
#include <SparkFunMLX90614.h>
//#include <SparkFunMPU9250-DMP.h>

// SERIAL
char serIn[100];
char serOut[100];

// ACTORS
// FastLED
#define NUM_LEDS 1
#define DATA_PIN 6
CRGB leds[NUM_LEDS];

// Servos
Servo thermoServo;
Servo ejectionServo;

// SENSORS
// APDS
//SparkFun_APDS9960 apds = SparkFun_APDS9960();
//uint16_t colors[4];

// Temp
IRTherm therm;
char dstr[13];
typedef struct {
    double object;
    double ambient;
} temp_t;
temp_t *t;

// 10Dof
/*
MPU9250_DMP _10dof;
float arr[3];*/
char double_str0[13];
char double_str1[13];
char double_str2[13];
unsigned char width = 12;
unsigned char prec = 5;

/**
 * Sets up the different modules.
 */
void setup() {
  Serial.begin(9600);
  setupFastLED();
  setupServos();
  //setupAPDS();
  setupTemp();
  //setup10dof();
}

/**
 * The main loop with the call of the main programm.
 */
void loop() {
  mainProg();
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
 * The main programm to responde to the serial getters and setters.
 */
void mainProg() {
  memset(&serIn, 0, sizeof(serIn));
  memset(&serOut, 0, sizeof(serOut));
  //memset(&double_str0, 0, sizeof(double_str0));
  //memset(&double_str1, 0, sizeof(double_str1));
  //memset(&double_str2, 0, sizeof(double_str2));
  while (!Serial.available()) { }
  read(serIn);
  // write(serIn);
  if (equals(serIn, ">getTemp")) {
        if (t = getTemperature()) {
            sprintf(serOut, "<temp:%s", dtostrf(t->object, width, prec, dstr));
        } else {
            sprintf(serOut, "<temp:null");
        }
    } /*else if (equals(serIn,  ">getAccel")) {
        if (getAccel(arr)) {
            sprintf(serOut, "<accel:%s,%s,%s",
                    dtostrf(arr[0], width, prec, double_str0),
                    dtostrf(arr[1], width, prec, double_str1),
                    dtostrf(arr[2], width, prec, double_str2)
            );
        } else {
            sprintf(serOut, "<accel:null");
        }
    } else if (equals(serIn, ">getGyro")) {
        if (getGyro(arr)) {
            sprintf(serOut, "<gyro:%s,%s,%s",
                    dtostrf(arr[0], width, prec, double_str0),
                    dtostrf(arr[1], width, prec, double_str1),
                    dtostrf(arr[2], width, prec, double_str2)
            );
        } else {
            sprintf(serOut, "<gyro:null");
        }
    } else if (equals(serIn, ">getMag")) {
        if (getMag(arr)) {
            sprintf(serOut, "<mag:%s,%s,%s",
                    dtostrf(arr[0], width, prec, double_str0),
                    dtostrf(arr[1], width, prec, double_str1),
                    dtostrf(arr[2], width, prec, double_str2)
            );
        } else {
            sprintf(serOut, "<mag:null");
        }
    } else if (equals(serIn, ">getColors")) {
        if (getColors((uint16_t *)colors)) {
            sprintf(serOut, "<colors:%i,%i,%i", colors[0], colors[1], colors[2]);
        } else {
            sprintf(serOut, "<colors:null");
        }
    } */else if (equals(serIn, ">setColor:")) {
        int num = 0;
        sscanf(serIn, ">setColor:%i", &num);
        displayColor(num);
        sprintf(serOut, "<setColor:%i", num);
    } else if (equals(serIn, ">setThermoServo:")) {
        int num = 0;
        sscanf(serIn, ">setThermoServo:%i", &num);
        thermoServo.write(num);
        sprintf(serOut, "<thermoServo:%i", num);
    } else if (equals(serIn, ">setEjectSpeed:")) {
        int num = 0;
        sscanf(serIn, ">setEjectSpeed:%i", &num);
        setSpeed(num);
        sprintf(serOut, "<speed:%i", num);
    } else {
        sprintf(serOut, "<null");
    }
    write(serOut);
    // 5 .. 1024
    // 3,7 .. x
    // x = 1024 / 5 * 3,7
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

/**
 * Sets up the FastLED library.
 */
void setupFastLED() {
  FastLED.addLeds<WS2812B, DATA_PIN, RGB>(leds, NUM_LEDS);
}

/**
 * Displays a HSV value on the RGB-LED.
 * 
 * @param color A color value in HSV.
 */
void displayColor(uint16_t color) {
  leds[0] = CHSV(color, 255, 255);
  FastLED.show();
}

/**
 * Sets up the Servos for the thermosensor and the ejection system.
 */
void setupServos() {
  //thermoServo.attach(3);
  //ejectionServo.attach(2);
}

/**
 * Sets the speed of the ejection servo.
 * 
 * @param The percent of speed from 0 - 100.
 */
void setSpeed(int percent) {
  ejectionServo.write(map(percent, 0, 100, 0, 180));
}

/**
 * Sets up the APDS (color sensor).
 */
 /*
void setupAPDS() {
  if ( !apds.init() ) {
    Serial.println("Something went wrong during APDS-9960 init!");
  }  
  if ( !apds.enableLightSensor(false) ) {
    Serial.println("Something went wrong during light sensor init!");
  }
}
*/
/**
 * Stores the values from the APDS sensor to the array.
 * 
 * @param The array to store the value to.
 * @return If everything worked (1) or if an error occured (0).
 */
/*
uint8_t getColors(uint16_t *arr) {
    uint16_t ambient_light = 0;
    uint16_t red_light = 0;
    uint16_t green_light = 0;
    uint16_t blue_light = 0;

    if (  !apds.readAmbientLight(ambient_light) ||
          !apds.readRedLight(red_light) ||
          !apds.readGreenLight(green_light) ||
          !apds.readBlueLight(blue_light) ) {
        return 0;
    }

    arr[0] = ambient_light;
    arr[1] = red_light;
    arr[2] = green_light;
    arr[3] = blue_light;

    return 1;
}
*/
/**
 * Sets up the temperature sensor.
 */
void setupTemp() {
  therm.begin();
  therm.setUnit(TEMP_C);
}

/**
 * Measures the temperature on the temperature sensor and return the pointer of the struct.
 * 
 * @return The struct of the temperatures measured, where object is the one far away and ambient the temperature directly on the sensor.
 */
temp_t *getTemperature() {
    temp_t temp;
    if (therm.read()) {
        temp.object = therm.object();
        temp.ambient = therm.ambient();
        //Serial.println(temp.ambient);
        return &temp;
    } else {
      write("Not working");
        return NULL;
    }
}

/**
 * Sets up the MPU9250 (10dof).
 */
 /*
void setup10dof() {
  if (_10dof.begin() != INV_SUCCESS)
  {
    while (1)
    {
      Serial.println("Unable to communicate with MPU-9250");
      Serial.println("Check connections, and try again.");
      Serial.println();
      delay(5000);
    }
  }

  _10dof.setSensors(INV_XYZ_GYRO); // Enable gyroscope only
  _10dof.setGyroFSR(2000); // Set gyro to 2000 dps

 /* _10dof.dmpBegin(DMP_FEATURE_GYRO_CAL |
              DMP_FEATURE_SEND_CAL_GYRO,
              10);/* */
//}

/**
 * Gets the values measured by the Accelerometer.
 * 
 * @param The array to store the values to.
 * @return An error code, where 0 an error occured.
 */

/*uint8_t getAccel(float *arr) {
    uint8_t err = _10dof.updateAccel();
    arr[0] = _10dof.calcAccel(_10dof.ax);
    arr[1] = _10dof.calcAccel(_10dof.ay);
    arr[2] = _10dof.calcAccel(_10dof.az);
    return err;
}
*/
/**
 * Gets the values measured by the Gyroscop.
 * 
 * @param The array to store the values to.
 * @return An error code, where 0 an error occured.
 */
/*
uint8_t getGyro(float *arr) {
    uint8_t err = _10dof.updateGyro();
    arr[0] = _10dof.calcGyro(_10dof.gx);
    arr[1] = _10dof.calcGyro(_10dof.gy);
    arr[2] = _10dof.calcGyro(_10dof.gz);
    return err;
}
*/
/**
 * Gets the values measured by the Magnetometer.
 * 
 * @param The array to store the values to.
 * @return An error code, where 0 an error occured.
 */
 /*
uint8_t getMag(float *arr) {
    uint8_t err = _10dof.updateCompass();
    arr[0] = _10dof.calcMag(_10dof.mx);
    arr[1] = _10dof.calcMag(_10dof.my);
    arr[2] = _10dof.calcMag(_10dof.mz);
    return err;
}
*/
