#pragma once

#include <functional>
#include <utility>

#include "Functions.h"

enum MODE
{
    NONE, TEST, Main1, Main2, Main3, Main4, OSC
};

struct Problem {
    //std::function<double(double)> f;
    //std::function<double(double)> df;
    //std::function<double(double)> d2f;

    MODE mode{NONE};
    double a{};
    double b{};
    double mu1{};
    double mu2{};

    /*explicit Problem(
        std::function<double(double)> f = [](double x) { return x; },
        std::function<double(double)> df = [](double x) { return 1; },
        std::function<double(double)> d2f = [](double x) { return 0; },
        double a = -1.0, double b = 1.0, double mu1 = 0.0, double mu2 = 0.0)
        : f(std::move(f)), df(std::move(df)), d2f(std::move(d2f)), a(a), b(b), mu1(mu1), mu2(mu2) {
    };*/

    explicit Problem();
    explicit Problem( MODE _mode);
    void operator=(const Problem& _problem);

    double f(double x);
    double df(double x);
    double d2f(double x);
};