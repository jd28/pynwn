#include <pybind11/pybind11.h>

namespace py = pybind11;

void init_locstring(py::module& m);

PYBIND11_MODULE(_libnw, m)
{
    m.doc() = "libnw python wrapper";

    init_locstring(m);
}
