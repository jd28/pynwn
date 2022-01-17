#include <pybind11/pybind11.h>

#include <nw/i18n/LocString.hpp>

namespace py = pybind11;

void init_locstring(py::module& m)
{
    py::class_<nw::LocString>(m, "LocString")
        .def(py::init<uint32_t>())
        .def(
            "__getitem__", [](nw::LocString& ls, uint32_t index) {
                return ls.get(index);
            })
        .def("add", &nw::LocString::add, "Add a string", py::arg("language"), py::arg("string"), py::arg("feminine") = false, py::arg("force_language") = false)
        .def("get", &nw::LocString::get)
        .def("size", &nw::LocString::size)
        .def("strref", &nw::LocString::strref);
}
