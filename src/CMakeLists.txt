find_package(Threads)

find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(_libnw NO_EXTRAS
    pynwn/wrapper.cpp

    pynwn/i18n/wrapper_i18n.cpp
    pynwn/i18n/wrapper_i18n_locstring.cpp


)

target_link_libraries(_libnw PRIVATE nw pybind11::module)

include(../cmake/Cache.cmake)

include(../cmake/CompilerWarnings.cmake)
set_project_warnings(_libnw)

target_include_directories(_libnw PRIVATE
    ../external/libnw/lib
    ../external/libnw/external
    ../external/pybind11_json/include
)
