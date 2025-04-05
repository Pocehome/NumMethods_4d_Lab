#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "Solver.h"
#include "Functions.h"
#include "Problems.h"

namespace py = pybind11;

PYBIND11_MODULE(Lab_Spline_Module, m) {
    py::class_<Solver>(m, "Solver")
        .def(py::init<int, MODE>())
        .def("Solve", &Solver::Solve)
        .def("getA", &Solver::getA)
        .def("getB", &Solver::getB)
        .def("getC", &Solver::getC)
        .def("getD", &Solver::getD)

        .def("getX_for_coef_table", &Solver::getX_for_coef_table)
        .def("getX", &Solver::getX)

        .def("getF", &Solver::getF)
        .def("getDF", &Solver::getDF)
        .def("getD2F", &Solver::getD2F)

        .def("getS", &Solver::getS)
        .def("getDS", &Solver::getDS)
        .def("getD2S", &Solver::getD2S)

        .def("getF_ERRROR", &Solver::getF_ERRROR)
        .def("getF_ERRROR_X", &Solver::getF_ERRROR_X)
        .def("getDF_ERRROR", &Solver::getDF_ERRROR)
        .def("getDF_ERRROR_X", &Solver::getDF_ERRROR_X)
        .def("getD2F_ERRROR", &Solver::getD2F_ERRROR)
        .def("getD2F_ERRROR_X", &Solver::getD2F_ERRROR_X)

        .def("get_n_step", &Solver::get_n_step)
        .def("get_N_step", &Solver::get_N_step);

    py::enum_<MODE>(m, "MODE")
        .value("NONE", MODE::NONE)
        .value("TEST", MODE::TEST)
        .value("Main1", MODE::Main1)
        .value("Main2", MODE::Main2)
        .value("Main3", MODE::Main3)
        .value("Main4", MODE::Main4)
        .value("OSC", MODE::OSC)
        .export_values();
}