#include <Arduino.h>
#include <math.h>
#include "motors.h"


StepperMotor::StepperMotor(unsigned int pins[4]):pins(pins), teeth(8), gearRatio(64), pos(0), coils(4), maxPwm(255) {
    for (int i = 0; i < this->coils; i++) {
        pinMode(this->pins[i], OUTPUT);
    }
};

void StepperMotor::hold() {
        float posCoils = fmod(pos, coils);
        if (posCoils == (int)posCoils) {
            for (int coil = 0; coil < coils; coil++) {  /*iterating through coils*/
                if (coil == posCoils) {
                    digitalWrite(pins[coil], 1*maxPwm);
                }
                else {
                    digitalWrite(pins[coil], 0);
                }
            }
        }
        else {
            int backward = fmod(floor(posCoils), coils);  // without mod it would be larger than coils
            int forward = fmod(ceil(posCoils), coils);  // without mod it would be larger than coils
            for (int coil = 0; coil < coils; coil++) {  /*iterating through coils*/
                if (coil == backward) {
                    digitalWrite(pins[coil], ((int) posCoils+1-posCoils)*maxPwm);
                }
                else if (coil == forward) {
                    digitalWrite(pins[coil], (posCoils - (int) posCoils)*maxPwm);
                }
                else {
                    digitalWrite(pins[coil], 0);
                }
            }
        }
};

void StepperMotor::release() {
    for (int coil = 0; coil < this->coils; coil++) {
        digitalWrite(this->pins[coil], 0);
    }
};

void StepperMotor::runContinously(float stepsize, float velocity) {
    isRunning = true;
    while (true) {
        if (isRunning == false){
            return;  // break the loop and do not continue anything
        }
        setPos(pos+stepsize);
        this->hold();
        delay(3*velocity);
    }
    isRunning = false;
};

void StepperMotor::runSteps(float steps, float stepsize, float velocity, bool hold) {
    if (steps < 0) {
        steps = abs(steps);
        stepsize *= -1;
    }
    this->isRunning = true;
    for (float step = 0; step <= steps; step += abs(stepsize)) {
        if (this->isRunning == false){
            return;  // break the loop and do not continue anything
        }
        setPos(pos+stepsize);
        this->hold();
        delay(3*velocity);
    }
    if (!hold) {
        release();
    }
    this->isRunning = false;
};

void StepperMotor::setPos(float pos) {
    // see: https://stackoverflow.com/questions/7594508/modulo-operator-with-negative-values
    this->pos = fmod(coils*teeth*gearRatio + fmod(pos, coils*teeth*gearRatio), coils*teeth*gearRatio);  // position can only be positive
}

void StepperMotor::setPosRad(double rad) {
    // Inaccuracies might occur based on the inaccuracy of PI.
    double factor = (coils*teeth*gearRatio) / (2*PI);
    setPos(rad*factor);
};

double StepperMotor::getPosRad() {
    // Inaccuracies might occur based on the inaccuracy of PI.
    double factor = (2*PI) / (coils*teeth*gearRatio);
    return pos * factor;
};

void StepperMotor::runAngleRad(float angle, float stepsize, float velocity, bool hold) {
    // Inaccuracies might occur based on the inaccuracy of PI.
    double factor = (coils*teeth*gearRatio) / (2*PI);
    runSteps(angle*factor, stepsize, velocity, hold);
};

void StepperMotor::runPosRad(float angle, float stepsize, float velocity, bool hold) {
    // Inaccuracies might occur based on the inaccuracy of PI.
    // Works only on positive stepsize.
    angle = fmod(2*PI + fmod(angle, 2*PI), 2*PI);
    runAngleRad(angle-getPosRad(), stepsize, velocity, hold);
};

void StepperMotor::stop(bool hold) {
    isRunning = false;
    if (hold) {
        this->hold();
    }
    else {
        release();
    }
};

void StepperMotor::setPosDeg(double deg) {
    double factor = (coils*teeth*gearRatio) / 360;
    setPos(deg*factor);
};

double StepperMotor::getPosDeg() {
    double factor = 360 / (coils*teeth*gearRatio);
    return pos * factor;
};

void StepperMotor::runAngleDeg(float angle, float stepsize, float velocity, bool hold) {
    double factor = (coils*teeth*gearRatio) / 360;
    runSteps(angle*factor, stepsize, velocity, hold);
};

void StepperMotor::runPosDeg(float angle, float stepsize, float velocity, bool hold) {
    // Works only on positive stepsize.
    angle = fmod(360 + fmod(angle, 360), 360);
    runAngleDeg(angle-getPosDeg(), stepsize, velocity, hold);
};

ButtonStepperMotor::ButtonStepperMotor(unsigned int pins[4], unsigned int buttonPin):StepperMotor(pins), buttonPin(buttonPin) {
    pinMode(this->buttonPin, INPUT);
};

void ButtonStepperMotor::runUntilButtonPressed(float stepsize, float velocity) {
    pinMode(this->buttonPin, INPUT);
    this->isRunning = true;
    while (true) {
        if (this->isRunning == false || digitalRead(this->buttonPin)) {
            this->release();
            return;  // break the loop and do not continue anything
        }
        this->setPos(this->pos+stepsize);
        this->hold();
        delay(3*velocity);
    }
    this->isRunning = false;
};