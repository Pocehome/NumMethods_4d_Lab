#include "Solver.h"
#include "Spline.h"

//Расчёт коэффициентов
Solver::Solver(int n, MODE _mode): n(n)
{
    Problem tmp_problem(_mode);
    problem = tmp_problem;

    n_step = (problem.b - problem.a) / n;

    double x = problem.a;
    while (x < problem.b - 1e-6) {
        spline.grid.emplace_back(x);
        f_vector.emplace_back(problem.f(x));
        x += n_step;
    }

    spline.grid.emplace_back(problem.b);
    f_vector.emplace_back(problem.f(problem.b));


    spline.A = std::vector<double>(n);
    spline.B = std::vector<double>(n);
    spline.C = std::vector<double>(n + 1);
    spline.D = std::vector<double>(n);
    spline.size = n;
}

void Solver::calcA() {
    spline.A = f_vector;
    spline.A.erase(spline.A.begin());
}

void Solver::calcB() {
    for (int i = 0; i < spline.size; ++i) {
        spline.B[i] = (f_vector[i + 1] - f_vector[i]) / n_step + spline.C[i + 1] * n_step / 3 + spline.C[i] * n_step / 6;
    }
}

void Solver::calcC() {
    std::vector<double> AB(n - 1, n_step);
    std::vector<double> C(n - 1, -4 * n_step);
    std::vector<double> phi(n - 1);
    for (int i = 0; i < n - 1; i++) {
        phi[i] = -6 * (f_vector[i + 2] - 2 * f_vector[i + 1] + f_vector[i]) / n_step;
    }

    //    double mu1 = (2.5*F[0] - 6*F[1] + 4.5*F[2] - F[3]) / step / step;
    //    double mu2 = (-F[n-3] + 4.5*F[n-2] - 6*F[n-1] + 2.5*F[n]) / step / step;

    spline.C = SolveTridiagonalMatrix(AB, C, AB, phi, { 0.0, 0.0 }, { problem.mu1, problem.mu2 });
    //    spline.C = SolveTridiagonalMatrix(AB, C, AB, phi, {-0.5, -0.5}, {mu1, mu2});
}

void Solver::calcD() {
    for (int i = 0; i < n; ++i) {
        spline.D[i] = (spline.C[i + 1] - spline.C[i]) / n_step;
    }
}


//Основыне функции
void Solver::Solve()
{
    spline = getSpline();

    N_step = (problem.b - problem.a) / (2 * n);

    double eps = 0.000000001;
    double xi = problem.a;
    while (xi <= problem.b + eps) {
        x_vector.emplace_back(xi);
        spline_vector.emplace_back(spline(xi));
        F_vector.emplace_back(problem.f(xi));
        d_s.emplace_back(spline.ds(xi));
        d2_s.emplace_back(spline.d2s(xi));
        d_f.emplace_back(problem.df(xi));
        d2_f.emplace_back(problem.d2f(xi));


        double tmp = std::abs(F_vector.back() - spline_vector.back());
        if (tmp > f_error) {
            f_error = tmp;
            x_of_f_err = xi;
        }

        tmp = std::abs(d_f.back() - d_s.back());
        if (tmp > df_error) {
            df_error = tmp;
            x_of_df_err = xi;
        }

        tmp = std::abs(d2_f.back() - d2_s.back());
        if (tmp > d2f_error) {
            d2f_error = tmp;
            x_of_d2f_err = xi;
        }

        xi += N_step;
    }
    int i = 0;
}

Spline& Solver::getSpline() {
    calcC();
    calcA();
    calcB();
    calcD();
    spline.C.erase(spline.C.begin());
    return spline;
}


//Геттеры
std::vector<double>& Solver::getA()
{
    return spline.A;
}

std::vector<double>& Solver::getB()
{
    return spline.B;
}

std::vector<double>& Solver::getC()
{
    return spline.C;
}

std::vector<double>& Solver::getD()
{
    return spline.D;
}

std::vector<double>& Solver::getX_for_coef_table()
{
    return spline.grid;
}

std::vector<double>& Solver::getX()
{
    return x_vector;
}

std::vector<double>& Solver::getF()
{
    return F_vector;
}

std::vector<double>& Solver::getDF()
{
    return d_f;
}

std::vector<double>& Solver::getD2F()
{
    return d2_f;
}

std::vector<double>& Solver::getS()
{
    return spline_vector;
}

std::vector<double>& Solver::getDS()
{
    return d_s;
}

std::vector<double>& Solver::getD2S()
{
    return d2_s;
}

double Solver::getF_ERRROR()
{
    return f_error;
}

double Solver::getF_ERRROR_X()
{
    return x_of_f_err;
}

double Solver::getDF_ERRROR()
{
    return df_error;
}

double Solver::getDF_ERRROR_X()
{
    return x_of_df_err;
}

double Solver::getD2F_ERRROR()
{
    return d2f_error;
}

double Solver::getD2F_ERRROR_X()
{
    return x_of_d2f_err;
}

double Solver::get_n_step()
{
    return n_step;
}

double Solver::get_N_step()
{
    return N_step;
}


