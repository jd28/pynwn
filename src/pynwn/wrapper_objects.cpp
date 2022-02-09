#include <nw/objects/Area.hpp>
#include <nw/objects/Creature.hpp>
#include <nw/objects/Door.hpp>
#include <nw/objects/Encounter.hpp>
#include <nw/objects/Item.hpp>
#include <nw/objects/Module.hpp>
#include <nw/objects/ObjectBase.hpp>
#include <nw/objects/Placeable.hpp>
#include <nw/objects/Sound.hpp>
#include <nw/objects/Store.hpp>
#include <nw/objects/Trigger.hpp>
#include <nw/objects/Waypoint.hpp>
#include <nw/objects/components/Common.hpp>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <pybind11_json/pybind11_json.hpp>

namespace py = pybind11;

PYBIND11_MAKE_OPAQUE(std::vector<glm::vec3>);
PYBIND11_MAKE_OPAQUE(std::vector<nw::InventoryItem>);

void init_object_components(py::module& m);

void init_objects_base(py::module& m)
{
    py::enum_<nw::ObjectID>(m, "ObjectID");
    m.attr("OBJECT_INVALID") = nw::object_invalid;

    py::enum_<nw::ObjectType>(m, "ObjectType")
        .value("invalid", nw::ObjectType::invalid)
        .value("gui", nw::ObjectType::gui)
        .value("tile", nw::ObjectType::tile)
        .value("module", nw::ObjectType::module)
        .value("area", nw::ObjectType::area)
        .value("creature", nw::ObjectType::creature)
        .value("item", nw::ObjectType::item)
        .value("trigger", nw::ObjectType::trigger)
        .value("projectile", nw::ObjectType::projectile)
        .value("placeable", nw::ObjectType::placeable)
        .value("door", nw::ObjectType::door)
        .value("areaofeffect", nw::ObjectType::areaofeffect)
        .value("waypoint", nw::ObjectType::waypoint)
        .value("encounter", nw::ObjectType::encounter)
        .value("store", nw::ObjectType::store)
        .value("portal", nw::ObjectType::portal)
        .value("sound", nw::ObjectType::sound);

    py::class_<nw::ObjectBase>(m, "ObjectBase")
        .def(py::init<>())
        //.def("as_area", py::overload_cast<>(&nw::ObjectBase::as_area), py::return_value_policy::reference_internal)
        //.def("as_area", py::overload_cast<>(&nw::ObjectBase::as_area, py::const_), py::return_value_policy::reference_internal)
        .def("common", py::overload_cast<>(&nw::ObjectBase::common), py::return_value_policy::reference_internal)
        .def("common", py::overload_cast<>(&nw::ObjectBase::common, py::const_), py::return_value_policy::reference_internal)
        .def("as_creature", py::overload_cast<>(&nw::ObjectBase::as_creature), py::return_value_policy::reference_internal)
        .def("as_creature", py::overload_cast<>(&nw::ObjectBase::as_creature, py::const_), py::return_value_policy::reference_internal)
        .def("as_door", py::overload_cast<>(&nw::ObjectBase::as_door), py::return_value_policy::reference_internal)
        .def("as_door", py::overload_cast<>(&nw::ObjectBase::as_door, py::const_), py::return_value_policy::reference_internal)
        .def("as_encounter", py::overload_cast<>(&nw::ObjectBase::as_encounter, py::const_), py::return_value_policy::reference_internal)
        // .def("as_item", py::overload_cast<>(&nw::ObjectBase::as_item), py::return_value_policy::reference_internal)
        // .def("as_item", py::overload_cast<>(&nw::ObjectBase::as_item, py::const_), py::return_value_policy::reference_internal)
        .def("as_module", py::overload_cast<>(&nw::ObjectBase::as_module), py::return_value_policy::reference_internal)
        .def("as_module", py::overload_cast<>(&nw::ObjectBase::as_module, py::const_), py::return_value_policy::reference_internal)
        // .def("as_placeable", py::overload_cast<>(&nw::ObjectBase::as_placeable), py::return_value_policy::reference_internal)
        // .def("as_placeable", py::overload_cast<>(&nw::ObjectBase::as_placeable, py::const_), py::return_value_policy::reference_internal)
        .def("as_sound", py::overload_cast<>(&nw::ObjectBase::as_sound), py::return_value_policy::reference_internal)
        .def("as_sound", py::overload_cast<>(&nw::ObjectBase::as_sound, py::const_), py::return_value_policy::reference_internal)
        // .def("as_store", py::overload_cast<>(&nw::ObjectBase::as_store), py::return_value_policy::reference_internal)
        // .def("as_store", py::overload_cast<>(&nw::ObjectBase::as_store, py::const_), py::return_value_policy::reference_internal)
        .def("as_trigger", py::overload_cast<>(&nw::ObjectBase::as_trigger), py::return_value_policy::reference_internal)
        .def("as_trigger", py::overload_cast<>(&nw::ObjectBase::as_trigger, py::const_), py::return_value_policy::reference_internal)
        .def("as_waypoint", py::overload_cast<>(&nw::ObjectBase::as_waypoint), py::return_value_policy::reference_internal)
        .def("as_waypoint", py::overload_cast<>(&nw::ObjectBase::as_waypoint, py::const_), py::return_value_policy::reference_internal);
}

void init_objects_area(py::module&) { }
void init_objects_creature(py::module&) { }
void init_objects_door(py::module&) { }
void init_objects_encounter(py::module&) { }
void init_objects_item(py::module&) { }
void init_objects_module(py::module&) { }
void init_objects_placeable(py::module&) { }
void init_objects_sound(py::module&) { }
void init_objects_store(py::module&) { }

void init_object_trigger(pybind11::module& m)
{
    pybind11::class_<nw::TriggerScripts>(m, "TriggerScripts")
        .def(pybind11::init<>())
        .def_readwrite("on_click", &nw::TriggerScripts::on_click)
        .def_readwrite("on_disarm", &nw::TriggerScripts::on_disarm)
        .def_readwrite("on_enter", &nw::TriggerScripts::on_enter)
        .def_readwrite("on_exit", &nw::TriggerScripts::on_exit)
        .def_readwrite("on_heartbeat", &nw::TriggerScripts::on_heartbeat)
        .def_readwrite("on_trap_triggered", &nw::TriggerScripts::on_trap_triggered)
        .def_readwrite("on_user_defined", &nw::TriggerScripts::on_user_defined);

    py::bind_vector<std::vector<glm::vec3>>(m, "VectorVec3");

    pybind11::class_<nw::Trigger, nw::ObjectBase>(m, "Trigger")
        .def(pybind11::init<>())
        .def(pybind11::init<nlohmann::json, nw::SerializationProfile>())
        .def("valid", &nw::Trigger::valid)
        .def_readonly_static("json_archive_version", &nw::Trigger::json_archive_version)
        .def_readwrite("scripts", &nw::Trigger::scripts)
        .def_readwrite("geometry", &nw::Trigger::geometry)
        .def_readwrite("linked_to", &nw::Trigger::linked_to)
        .def_readwrite("highlight_height", &nw::Trigger::highlight_height)
        .def_readwrite("type", &nw::Trigger::type)
        .def_readwrite("faction", &nw::Trigger::faction)
        .def_readwrite("loadscreen", &nw::Trigger::loadscreen)
        .def_readwrite("portrait", &nw::Trigger::portrait)
        .def_readwrite("cursor", &nw::Trigger::cursor)
        .def_readwrite("linked_to_flags", &nw::Trigger::linked_to_flags);
}

void init_object_waypoint(pybind11::module& m)
{
    pybind11::class_<nw::Waypoint, nw::ObjectBase>(m, "Waypoint")
        .def(pybind11::init<>())
        .def(pybind11::init<nlohmann::json, nw::SerializationProfile>())
        .def_readwrite("description", &nw::Waypoint::description)
        .def_readwrite("linked_to", &nw::Waypoint::linked_to)
        .def_readwrite("map_note", &nw::Waypoint::map_note)
        .def_readwrite("appearance", &nw::Waypoint::appearance)
        .def_readwrite("has_map_note", &nw::Waypoint::has_map_note)
        .def_readwrite("map_note_enabled", &nw::Waypoint::map_note_enabled);
}

void init_objects(py::module& m)
{
    init_object_components(m);
    init_objects_base(m);
    init_objects_area(m);
    init_objects_creature(m);
    init_objects_door(m);
    init_objects_encounter(m);
    init_objects_item(m);
    init_objects_module(m);
    init_objects_placeable(m);
    init_objects_sound(m);
    init_objects_store(m);
    init_object_trigger(m);
    init_object_waypoint(m);
}
