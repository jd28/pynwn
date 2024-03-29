cmake_minimum_required(VERSION 3.21)
project(pynwn VERSION 0.1.0 LANGUAGES CXX C)
set (CMAKE_CXX_STANDARD 20)

if(MSVC)
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")

    add_definitions(
        /bigobj
        -D_CRT_SECURE_NO_WARNINGS
        -DUNICODE
        -D_UNICODE
        -D_SILENCE_ALL_CXX17_DEPRECATION_WARNINGS # abseil
        -DSTBI_WINDOWS_UTF8 # stbi_image
    )
endif()

include(cmake/PreventInSourceBuilds.cmake)
include(cmake/ProjectSettings.cmake)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# AppleClang changes visibility to hidden
if(CMAKE_CXX_COMPILER_ID MATCHES ".*Clang" OR CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  add_compile_options(-fvisibility=hidden)
endif()

add_subdirectory(external/libnw)
add_subdirectory(external/pybind11)
add_subdirectory(src)
