#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(nw_wrapper, m)
{
    m.doc() = "libnw python wrapper";
}
