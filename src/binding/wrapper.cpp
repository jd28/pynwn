#include "glm/wrap_vmath.h"
#include "opaque_types.hpp"

#include <pybind11/pybind11.h>

namespace py = pybind11;

void init_formats(py::module& nw);
void init_i18n(py::module& nw);
void init_objects(py::module& nw);
void init_resources(py::module& nw);
void init_serialization(py::module& nw);
void init_util(py::module& nw);

void init_kernel(py::module& nw, py::module& kernel);

PYBIND11_MODULE(_libnw, nw)
{
    nw.doc() = "libnw python wrapper";

    // pybind11 doesn't have native type for this.
    py::class_<std::filesystem::path>(nw, "Path")
        .def(py::init<std::string>())
        .def("__repr__", [](const std::filesystem::path& self) {
            return self.u8string();
        });
    py::implicitly_convertible<std::string, std::filesystem::path>();

    bind_opaque_types(nw);
    // Initialize submodules
    init_formats(nw);
    init_i18n(nw);
    init_objects(nw);
    init_resources(nw);
    init_serialization(nw);
    init_util(nw);
    wrap_vmath(nw);

    py::module kernel = nw.def_submodule("kernel");
    init_kernel(nw, kernel);
}
