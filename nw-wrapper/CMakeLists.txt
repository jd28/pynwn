find_package(Threads)

find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(nw-wrapper NO_EXTRAS
    wrapper.cpp

    i18n/wrapper_locstring.cpp
)

target_link_libraries(nw-wrapper PRIVATE nw pybind11::module)

include(../cmake/ProjectSettings.cmake)
include(../cmake/PreventInSourceBuilds.cmake)

target_compile_features(nw-wrapper INTERFACE cxx_std_17)

include(../cmake/Cache.cmake)

include(../cmake/CompilerWarnings.cmake)
set_project_warnings(nw-wrapper)

include(../cmake/Sanitizers.cmake)
enable_sanitizers(nw-wrapper)

target_include_directories(nw-wrapper PRIVATE ../external/libnw/lib)
