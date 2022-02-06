#include <nw/objects/ObjectBase.hpp>
#include <nw/objects/Waypoint.hpp>
#include <nw/objects/components/Common.hpp>

#include <pybind11/pybind11.h>

void init_objects_base(pybind11::module& m)
{
    pybind11::enum_<nw::ObjectID>(m, "ObjectID");
    m.attr("OBJECT_INVALID") = nw::object_invalid;

    pybind11::enum_<nw::ObjectType>(m, "ObjectType")
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

    pybind11::class_<nw::ObjectBase>(m, "ObjectBase")
        .def(pybind11::init<>())
        // .def("as_area", pybind11::overload_cast<>(&nw::ObjectBase::as_area))
        // .def("as_area", pybind11::overload_cast<>(&nw::ObjectBase::as_area, pybind11::const_))
        .def("common", pybind11::overload_cast<>(&nw::ObjectBase::common), pybind11::return_value_policy::reference_internal)
        .def("common", pybind11::overload_cast<>(&nw::ObjectBase::common, pybind11::const_), pybind11::return_value_policy::reference_internal)
        // .def("as_creature", pybind11::overload_cast<>(&nw::ObjectBase::as_creature))
        // .def("as_creature", pybind11::overload_cast<>(&nw::ObjectBase::as_creature, pybind11::const_))
        // .def("as_door", pybind11::overload_cast<>(&nw::ObjectBase::as_door))
        // .def("as_door", pybind11::overload_cast<>(&nw::ObjectBase::as_door, pybind11::const_))
        // .def("as_encounter", pybind11::overload_cast<>(&nw::ObjectBase::as_encounter, pybind11::const_))
        // .def("as_item", pybind11::overload_cast<>(&nw::ObjectBase::as_item))
        // .def("as_item", pybind11::overload_cast<>(&nw::ObjectBase::as_item, pybind11::const_))
        // .def("as_module", pybind11::overload_cast<>(&nw::ObjectBase::as_module))
        // .def("as_module", pybind11::overload_cast<>(&nw::ObjectBase::as_module, pybind11::const_))
        // .def("as_placeable", pybind11::overload_cast<>(&nw::ObjectBase::as_placeable))
        // .def("as_placeable", pybind11::overload_cast<>(&nw::ObjectBase::as_placeable, pybind11::const_))
        // .def("as_sound", pybind11::overload_cast<>(&nw::ObjectBase::as_sound))
        // .def("as_sound", pybind11::overload_cast<>(&nw::ObjectBase::as_sound, pybind11::const_))
        // .def("as_store", pybind11::overload_cast<>(&nw::ObjectBase::as_store))
        // .def("as_store", pybind11::overload_cast<>(&nw::ObjectBase::as_store, pybind11::const_))
        // .def("as_trigger", pybind11::overload_cast<>(&nw::ObjectBase::as_trigger))
        // .def("as_trigger", pybind11::overload_cast<>(&nw::ObjectBase::as_trigger, pybind11::const_))
        .def("as_waypoint", pybind11::overload_cast<>(&nw::ObjectBase::as_waypoint), pybind11::return_value_policy::reference_internal)
        .def("as_waypoint", pybind11::overload_cast<>(&nw::ObjectBase::as_waypoint, pybind11::const_), pybind11::return_value_policy::reference_internal);
}
