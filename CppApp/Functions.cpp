#include "Functions.h"

double TestFunc(double x) {
    if (x >= -1.0 && x <= 0.0)
        return x * x * x + 3.0 * x * x;
    else if (x >= 0.0 && x <= 1.0)
        return -x * x * x + 3.0 * x * x;
}

double dTF(double x) {
    if (x >= -1.0 && x <= 0.0)
        return 3.0*x*x + 6*x;
    else if (x >= 0.0 && x <= 1.0)
        return -3.0*x * x + 3.0 * x;
}

double d2TF(double x) {
    if (x >= -1.0 && x <= 0.0)
        return 6.0 * x + 6.0;
    else if (x >= 0.0 && x <= 1.0)
        return -6.0 * x + 6.0;
}


double MainFunc1(double x) {
    return std::sqrt(x * x - 1.0) / x;
}

double dF1(double x) {
    return 1.0 / std::sqrt(x * x - 1) - std::sqrt(x * x - 1) / (x * x);
}

double d2F1(double x) {
    return -2.0 * x / std::pow(x * x - 1, 1.5) 
           - (1.0 / (x * std::sqrt(x * x - 1)) 
           - (2.0 * std::sqrt(x * x - 1)) / (x * x * x));
}


double MainFunc2(double x) {
    return pow(1.0 + x * x, 1.0 / 3.0);
}

double dF2(double x) {
    return (2 * x) / (3 * std::pow(1 + x * x, 2.0 / 3.0));
}

double d2F2(double x) {
    return (18 + 14 * x * x) / (27 * std::pow(1 + x * x, 5.0 / 3.0));
}


double MainFunc3(double x) {
    return sin(x + 1.0) / (x + 1.0);
}

double dF3(double x) {
    return ((x + 1) * std::cos(x + 1) - std::sin(x + 1)) / ((x + 1) * (x + 1));
}

double d2F3(double x) {
    return (-(x + 1) * (x + 1) * (x + 1) * std::sin(x + 1) - (x + 1) * (x + 1) 
           * std::cos(x + 1) + 2 * (x + 1) * std::sin(x + 1)) / std::pow(x + 1, 4);
}


double MainFunc4(double x) {
    return log1p(x) / (x + 1.0);
}

double dF4(double x) {
    return (1 - log1p(x)) / ((x + 1.0) * (x + 1.0));
}

double d2F4(double x) {
    return (2 * log1p(x) - 3) / ((x + 1.0) * (x + 1.0) * (x + 1.0));
}


double OscFunc(double x)
{
    return  std::sqrt(x * x - 1.0) / x + std::cos(10*x);
}

double dFosc(double x)
{
    return (x / std::sqrt(x * x - 1.0)) - (std::sqrt(x * x - 1.0) / (x * x)) 
            - 10.0 * std::sin(10.0 * x);
}

double d2Fosc(double x)
{
    return -1.0 / std::pow(x * x - 1.0, 1.5) -
            ((x / ((x * x - 1.0) * x * x)) - (2.0 * std::sqrt(x * x - 1.0) / (x * x * x))) -
            100.0 * std::cos(10.0 * x);
}
