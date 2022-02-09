find_package(Threads)

pybind11_add_module(_libnw NO_EXTRAS
    pynwn/wrapper.cpp

    pynwn/glm/glm_util.cpp
    pynwn/glm/wrap_vmath.cpp

    pynwn/wrapper_i18n.cpp
    pynwn/wrapper_objects_components.cpp
    pynwn/wrapper_objects.cpp
    pynwn/wrapper_serialization.cpp
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
