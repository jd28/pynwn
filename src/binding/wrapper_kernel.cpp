#include <nw/kernel/Kernel.hpp>
#include <nw/objects/Module.hpp>

#include <pybind11/pybind11.h>

#include <filesystem>

namespace py = pybind11;

void init_kernel_config(py::module& nw, py::module& kernel)
{
    py::class_<nw::ConfigOptions>(nw, "ConfigOptions")
        .def(py::init<>())
        .def_readwrite("version", &nw::ConfigOptions::version)
        .def_readwrite("install", &nw::ConfigOptions::install)
        .def_readwrite("user", &nw::ConfigOptions::user)
        .def_readwrite("include_install", &nw::ConfigOptions::include_install)
        .def_readwrite("include_nwsync", &nw::ConfigOptions::include_nwsync);
}

void init_kernel(py::module& nw, py::module& kernel)
{
    init_kernel_config(nw, kernel);
    kernel.def("load_module", &nw::kernel::load_module)
        .def("unload_module", &nw::kernel::unload_module);
}
