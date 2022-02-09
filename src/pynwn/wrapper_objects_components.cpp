#include <nw/objects/components/Appearance.hpp>
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

void init_component_appearance(py::module& m)
{
    py::class_<nw::BodyParts>(m, "BodyParts")
        .def(py::init<>())
        .def_readwrite("head", &nw::BodyParts::head)
        .def_readwrite("belt", &nw::BodyParts::belt)
        .def_readwrite("bicep_left", &nw::BodyParts::bicep_left)
        .def_readwrite("foot_left", &nw::BodyParts::foot_left)
        .def_readwrite("forearm_left", &nw::BodyParts::forearm_left)
        .def_readwrite("hand_left", &nw::BodyParts::hand_left)
        .def_readwrite("shin_left", &nw::BodyParts::shin_left)
        .def_readwrite("shoulder_left", &nw::BodyParts::shoulder_left)
        .def_readwrite("thigh_left", &nw::BodyParts::thigh_left)
        .def_readwrite("neck", &nw::BodyParts::neck)
        .def_readwrite("pelvis", &nw::BodyParts::pelvis)
        .def_readwrite("bicep_right", &nw::BodyParts::bicep_right)
        .def_readwrite("foot_right", &nw::BodyParts::foot_right)
        .def_readwrite("forearm_right", &nw::BodyParts::forearm_right)
        .def_readwrite("hand_right", &nw::BodyParts::hand_right)
        .def_readwrite("shin_right", &nw::BodyParts::shin_right)
        .def_readwrite("shoulder_right", &nw::BodyParts::shoulder_right)
        .def_readwrite("thigh_right", &nw::BodyParts::thigh_right);

    py::class_<nw::Appearance>(m, "Appearance")
        .def(py::init<>())
        .def_readwrite("phenotype", &nw::Appearance::phenotype)
        .def_readwrite("tail", &nw::Appearance::tail)
        .def_readwrite("wings", &nw::Appearance::wings)
        .def_readwrite("id", &nw::Appearance::id)
        .def_readwrite("portrait_id", &nw::Appearance::portrait_id)
        .def_readwrite("body_parts", &nw::Appearance::body_parts)
        .def_readwrite("hair", &nw::Appearance::hair)
        .def_readwrite("skin", &nw::Appearance::skin)
        .def_readwrite("tattoo1", &nw::Appearance::tattoo1)
        .def_readwrite("tattoo2", &nw::Appearance::tattoo2);
}

void init_object_components(py::module& m)
{
    py::module c = m.def_submodule("components", "Object components");
    init_component_common(c);
    init_component_localdata(c);
    init_component_location(c);
    init_component_appearance(c);
}
