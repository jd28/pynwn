#include <pybind11/pybind11.h>

namespace py = pybind11;

void init_i18n(py::module& m);

PYBIND11_MODULE(_libnw, m)
{
    m.doc() = "libnw python wrapper";

    // Initialize submodules
    init_i18n(m);
}
