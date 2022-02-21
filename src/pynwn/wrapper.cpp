#include "glm/wrap_vmath.h"
#include "opaque_types.hpp"

#include <pybind11/pybind11.h>

namespace py = pybind11;

void init_i18n(py::module& m);
void init_objects(py::module& m);
void init_resources(py::module& m);
void init_serialization(py::module& m);

PYBIND11_MODULE(_libnw, m)
{
    m.doc() = "libnw python wrapper";

    bind_opaque_types(m);
    // Initialize submodules
    init_i18n(m);
    init_objects(m);
    init_resources(m);
    init_serialization(m);
    wrap_vmath(m);
}
