#include <pybind11/pybind11.h>

#include "glm/wrap_vmath.h"

namespace py = pybind11;

void init_i18n(py::module& m);
void init_objects(py::module& m);
void init_serialization(py::module& m);

PYBIND11_MODULE(_libnw, m)
{
    m.doc() = "libnw python wrapper";

    // Initialize submodules
    init_i18n(m);
    init_objects(m);
    init_serialization(m);
    wrap_vmath(m);
}
