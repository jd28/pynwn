#include <nw/objects/components/Common.hpp>

#include <pybind11/pybind11.h>
#include <pybind11_json/pybind11_json.hpp>

namespace py = pybind11;

void init_component_common(py::module& m)
{
    py::class_<nw::Common>(m, "Common")
        .def(py::init<>())
        .def_readwrite("id", &nw::Common::id)
        .def_readwrite("object_type", &nw::Common::object_type)
        .def_readwrite("resref", &nw::Common::resref)
        .def_readwrite("tag", &nw::Common::tag)
        .def_readwrite("name", &nw::Common::name)
        .def_readwrite("local_data", &nw::Common::local_data)
        .def_readwrite("location", &nw::Common::location)
        .def_readwrite("comment", &nw::Common::comment)
        .def_readwrite("palette_id", &nw::Common::palette_id);
}

void init_component_localdata(py::module& m)
{
    pybind11::class_<nw::LocalData>(m, "LocalData")
        .def(py::init<>())
        .def("get_local_float", &nw::LocalData::get_local_float)
        .def("get_local_int", &nw::LocalData::get_local_int)
        .def("get_local_object", &nw::LocalData::get_local_object)
        .def("get_local_string", &nw::LocalData::get_local_string)
        .def("get_local_location", &nw::LocalData::get_local_location)
        .def("size", &nw::LocalData::size);
}

void init_component_location(py::module& m)
{
    pybind11::class_<nw::Location>(m, "Location")
        .def(py::init<>());
}

void init_object_components(py::module& m)
{
    py::module c = m.def_submodule("components", "Object components");
    init_component_common(c);
    init_component_localdata(c);
    init_component_location(c);
}
