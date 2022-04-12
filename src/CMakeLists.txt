find_package(Threads)

pybind11_add_module(pynwn NO_EXTRAS
    wrapper.cpp
    opaque_types.cpp

    glm/glm_util.cpp
    glm/wrap_vmath.cpp

    wrapper_formats.cpp
    wrapper_i18n.cpp
    wrapper_kernel.cpp
    wrapper_objects_components.cpp
    wrapper_objects.cpp
    wrapper_resources.cpp
    wrapper_serialization.cpp
    wrapper_util.cpp
)

target_link_libraries(pynwn PRIVATE nw pybind11::module)

include(../cmake/Cache.cmake)

include(../cmake/CompilerWarnings.cmake)
set_project_warnings(pynwn)

target_include_directories(pynwn PRIVATE
    ../external/libnw/lib
    ../external/libnw/external
    ../external/pybind11_json/include
    ../external/pybind11/include
)
