#include "motors.h"
#include <math.h>
#include <Wire.h>
#include "VL53L1X.h"


const float xCircumference = 16.31555*PI,
            yCircumference = 16.36183*PI;
unsigned int xMotorPins[4] = {4, 5, 6, 7},
             yMotorPins[4] = {10, 11, 12, 13};
ButtonStepperMotor xMotor(xMotorPins, 3),
                   yMotor(yMotorPins, 2);
VL53L1X Distance_Sensor;


void sendDistance(float xPosition, float yPosition, int numberSamples) {
    // TODO: Use sensor properly by toggling the timing.
    float distanceSum = 0;
    for (int sample = 0; sample < numberSamples; sample++) {
        distanceSum += Distance_Sensor.read();
    }
    Serial.println((String) xPosition + "," + (String) yPosition + "," + (String) (distanceSum / numberSamples) + ",");
}


void setup() {
    Wire.begin();
    Wire.setClock(400000); // use 400 kHz I2C
    Serial.begin(115200);

    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, 1);
    
    while (true) {
        while (Serial.available() == 0);
        if (Serial.readStringUntil('\n') == "connection request") {
            Serial.println("connection confirmation");
            while (Serial.available() == 0);
            if (Serial.readStringUntil('\n') == "connection acknowledgement") {
                break;
            }
        }
    }
    while (Serial.available() == 0);
    float xDistance = Serial.readStringUntil('\n').toFloat();
    while (Serial.available() == 0);
    float yDistance = Serial.readStringUntil('\n').toFloat();
    while (Serial.available() == 0);
    float xDistanceStep = Serial.readStringUntil('\n').toFloat();
    while (Serial.available() == 0);
    float yDistanceStep = Serial.readStringUntil('\n').toFloat();
    while (Serial.available() == 0);
    int numMeasurements = Serial.readStringUntil('\n').toFloat();

    while (Serial.available() == 0);
    if (Serial.readStringUntil('\n') == "__start__") {
        xMotor.runUntilButtonPressed(-1, 1.1);
        for (int xPosition = 0; xPosition <= xDistance; xPosition+=xDistanceStep) {
            // TODO: Initialize the sensor only once.
            Distance_Sensor.setTimeout(500);
            if (!Distance_Sensor.init()) {
                return;
            }
            Distance_Sensor.setDistanceMode(VL53L1X::Short);
            Distance_Sensor.setMeasurementTimingBudget(50000);
            Distance_Sensor.startContinuous(50);
            yMotor.runUntilButtonPressed(1, 1.1);
            int yPosition = 0;
            for (; yPosition <= yDistance; yPosition+=yDistanceStep) {
                sendDistance(xPosition, yPosition, numMeasurements);
                yMotor.runAngleDeg((-1 * 360) / yCircumference, .5, 1.1, false);
            }
            yPosition-=yDistanceStep;
            xMotor.runAngleDeg((1 * 360) / xCircumference, .5, 1.1, false);
            xPosition += xDistanceStep;
            for (; yPosition >= 0; yPosition-=yDistanceStep) {
                sendDistance(xPosition, yPosition, numMeasurements);
                yMotor.runAngleDeg((1 * 360) / yCircumference, .5, 1.1, false);
            }
            xMotor.runAngleDeg((1 * 360) / xCircumference, .5, 1.1, false);
        }
        Serial.println("__close__");
    }
    digitalWrite(LED_BUILTIN, 0);
}

void loop() {}
