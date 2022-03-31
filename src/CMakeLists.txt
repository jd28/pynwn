find_package(Threads)

pybind11_add_module(_libnw NO_EXTRAS
    binding/wrapper.cpp
    binding/opaque_types.cpp

    binding/glm/glm_util.cpp
    binding/glm/wrap_vmath.cpp

    binding/wrapper_formats.cpp
    binding/wrapper_i18n.cpp
    binding/wrapper_kernel.cpp
    binding/wrapper_objects_components.cpp
    binding/wrapper_objects.cpp
    binding/wrapper_resources.cpp
    binding/wrapper_serialization.cpp
    binding/wrapper_util.cpp
)

target_link_libraries(_libnw PRIVATE nw pybind11::module)

include(../cmake/Cache.cmake)

include(../cmake/CompilerWarnings.cmake)
set_project_warnings(_libnw)

target_include_directories(_libnw PRIVATE
    ../external/libnw/lib
    ../external/libnw/external
    ../external/pybind11_json/include
    ../external/pybind11/include
)
