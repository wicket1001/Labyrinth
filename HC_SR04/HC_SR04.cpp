/**
 * @author Harald Moritz
 * A HC_SR04 library for up to 4 HC_SR04s.
 */
#include "HC_SR04.h"

/**
 * Initialises the HC_SR04 library and set the trigger pins to output pins.
 * Please follow the port layout.
 *
 * D2 - D5 | PD2 - PD5 |    Echo |  Input
 * D6 - D7 | PD6 - PD7 | Trigger | Output
 * D2 = Front, D3 = Right, D4 = Back, D5 = Left
 * D6 = Front & Right, D7 = Back & Left
 */
HC_SR04::HC_SR04() {
    // DDRx  = pinMode         (read / write)
    // PINx  = pinValue        (read)
    // PORTx = pinManipulation (read / write)

    // Pin:
    // B11111100
    // B10101010
    //  76543210

    // DDRx:
    // Output = 1
    // Input  = 0

    // PORTx:
    // HIGH = 1
    // LOW  = 0

    DDRD |= B11000000;
}

/**
 * Gets the ultrasonic distances in cm.
 *
 * @param distances A double array to store the distances.
 */
boolean HC_SR04::getDistances(double distances[]) {
    uint8_t length = sizeof(distances) / sizeof(distances[0]);
    int raw[length];
    getRaw(raw);
    for (int i = 0; i < length; ++i) {
        distances[i] = raw[i] * 0.01716;
    }
    return true;
}

/**
 * Gets the raw difference in millis between the trigger and the echo of the ultrasonic sensors.
 *
 * @param raw An int array to store the raw difference in millis.
 */
void HC_SR04::getRaw(int raw[]) {
    uint8_t index = 0; // The index of the incoming pulse changes.
    uint8_t length = 9; // Num US * 2, because ON & OFF gespeichert werden + 1 because of inital state
    unsigned long pulses[length];
    uint8_t values[length];
    for (uint8_t i = 0; i < length; i ++) {
        pulses[i] = -1;
        values[i] = -1;
    }

    long counter = 0; // 859403
    values[index] = PORTD; // Saves the initial register value.
    PORTD &= B00111111; // Sets Triggers to Low
    delay(5);
    PORTD |= B11000000; // Sets Triggers to High
    delay(10);
    PORTD &= B00111111; // Sets Triggers to Low

    pulses[index] = millis() + timeout; // Saves the timeout time.
    index ++;
    while (millis() < pulses[0]) { // Store everything until the timeout.
        if (1 != PORTD) { // If something changes.
            Serial.print("Something changed: ");
            Serial.println(PORTD);
            if (index == length) { // If too many changes had happend.
                // Serial.println("I need more space. ~US");
                break;
            }
            pulses[index] = millis(); // Save the time something changed.
            values[index] = PORTD; // Save the change.
            index++;
        }
        counter ++;
    }
    Serial.print("Cycles: ");
    Serial.println(counter);

    pulses[0] -= timeout; // Change back to the real start time.
    for (uint8_t i = 1; i < length; i ++) { // Go through all changes.
        if (values[i - 1] < values[i]) { // If an input trigger got activated.
            uint8_t pin = lb(values[i] - values[i - 1]) - 2; // Get the pin of the next pulse.
            raw[pin] = pulses[i] - pulses[0]; // Write the time difference in the right raw position.
        }
    }
}

/**
 * Calculates the binary logarithm for a value < 256, which is a exponential of 2.
 *
 * @param value An exponential of 2 < 256.
 * @return The exponent of the value and by an error -1.
 */
uint8_t HC_SR04::lb(uint8_t value) {
    uint8_t ld = 0;
    boolean err = true;
    for (; ld < 7; ld ++) {
        if (value == 1) {
            err = false;
            break;
        }
        value = value >> 1;
    }
    return err ? -1 : ld;
}

/**
 * A self written pulseIn function.
 *
 * @param pin
 * @param state
 * @return
 */
unsigned long HC_SR04::pulseInA(uint8_t pin, uint8_t state) {

    unsigned long pulseWidth = 0;
    unsigned long loopCount = 0;
    unsigned long loopMax = 5000000;

    // While the pin is *not* in the target state we make sure the timeout hasn't been reached.
    while ((digitalRead(pin)) != state) {
        if (loopCount++ == loopMax) {
            return 0;
        }
    }

    // When the pin *is* in the target state we bump the counter while still keeping track of the timeout.
    while ((digitalRead(pin)) == state) {
        if (loopCount++ == loopMax) {
            return 0;
        }
        pulseWidth++;
    }

    // Return the pulse time in microsecond!
    //Serial.print("pulseWidth: ");
    //Serial.println(pulseWidth);
    return pulseWidth * 4.0; // Calculated the pulseWidth++ loop to be about 2.36uS in length.
}
