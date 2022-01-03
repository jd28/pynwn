cmake_minimum_required(VERSION 3.21)
project(pynwn VERSION 0.1.0 LANGUAGES CXX C)
set (CMAKE_CXX_STANDARD 17)

if(MSVC)
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")

    add_definitions(
        -D_CRT_SECURE_NO_WARNINGS
        -DUNICODE
        -D_UNICODE
        -D_SILENCE_ALL_CXX17_DEPRECATION_WARNINGS # abseil
        -DSTBI_WINDOWS_UTF8 # stbi_image
    )
endif()

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

add_subdirectory(external/libnw)
add_subdirectory(nw-wrapper)
