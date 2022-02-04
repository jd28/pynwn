#include <pybind11/pybind11.h>

namespace py = pybind11;

void init_i18n_locstring(py::module& m);

void init_i18n(py::module& m)
{
    py::module i18n = m.def_submodule("i18n", "internationalization related classes and functions");

    init_i18n_locstring(i18n);
}
