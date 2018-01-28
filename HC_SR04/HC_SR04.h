#ifndef __HC_SR04_H__
#define __HC_SR04_H__

#include <Arduino.h>

class HC_SR04 {
public:
    HC_SR04();
    boolean getDistances(double distances[]);
    void getRaw(int raw[]);
    double measureOne(uint8_t trigger, uint8_t echo);
    unsigned long pulseInSingle(uint8_t pin, uint8_t state);
private:
    int timeout = 2000;
    uint8_t lb(uint8_t value);
};

#endif
