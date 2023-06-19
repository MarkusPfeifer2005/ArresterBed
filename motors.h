#ifndef MOTORS_H
#define MOTORS_H


class StepperMotor{
public:
    unsigned int coils;     // 4
    unsigned int *pins;     // pointer variable
    unsigned int teeth;     // 8 teeth per coil
    unsigned int maxPwm;   // the maximum PWM signal, that is equivalent to digital 1
    float gearRatio;       // 64
    float pos;              // given in steps(an internal unit); relative to origin; requires getter & setter; max: coils*teeth*gear_ratio
    bool isRunning = false;

    StepperMotor(unsigned int pins[4]);
    void setPos(float pos);
    void runSteps(float steps, float stepsize, float velocity, bool hold);
    void runAngleRad(float angle, float stepsize, float velocity, bool hold);
    void runPosRad(float angle, float stepsize, float velocity, bool hold);
    void runContinously(float stepsize, float velocity);
    void stop(bool hold);
    void hold();
    void release();
    void setPosRad(double rad);
    double getPosRad();
    void setPosDeg(double deg);
    double getPosDeg();
    void runAngleDeg(float angle, float stepsize, float velocity, bool hold);
    void runPosDeg(float angle, float stepsize, float velocity, bool hold);
};

class ButtonStepperMotor: public StepperMotor {
public:
    unsigned int buttonPin;

    ButtonStepperMotor(unsigned int pins[4], unsigned int buttonPin);
    void ButtonStepperMotor::runUntilButtonPressed(float stepsize, float velocity);
};


#endif
