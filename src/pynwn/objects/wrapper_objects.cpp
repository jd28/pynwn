#include <pybind11/pybind11.h>

namespace py = pybind11;

void init_object_components(py::module& m);
void init_objects_base(py::module& m);
void init_object_waypoint(py::module& m);

void init_objects(py::module& m)
{
    init_object_components(m);
    init_objects_base(m);
    init_object_waypoint(m);
}
