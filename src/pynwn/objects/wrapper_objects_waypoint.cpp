#include <nw/objects/Waypoint.hpp>

#include <pybind11/pybind11.h>
#include <pybind11_json/pybind11_json.hpp>

void init_object_waypoint(pybind11::module& m)
{
    pybind11::class_<nw::Waypoint, nw::ObjectBase>(m, "Waypoint")
        .def(pybind11::init<>())
        .def(pybind11::init<nlohmann::json, nw::SerializationProfile>())
        .def_readwrite("common_", &nw::Waypoint::common_)
        .def_readwrite("description", &nw::Waypoint::description)
        .def_readwrite("linked_to", &nw::Waypoint::linked_to)
        .def_readwrite("map_note", &nw::Waypoint::map_note)
        .def_readwrite("appearance", &nw::Waypoint::appearance)
        .def_readwrite("has_map_note", &nw::Waypoint::has_map_note)
        .def_readwrite("map_note_enabled", &nw::Waypoint::map_note_enabled);
}
