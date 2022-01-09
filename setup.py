from setuptools import find_packages
import os
import re
import subprocess
import sys

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext

# Convert distutils Windows platform specifiers to CMake -A arguments
PLAT_TO_CMAKE = {
    "win32": "Win32",
    "win-amd64": "x64",
    "win-arm32": "ARM",
    "win-arm64": "ARM64",
}


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(
            self.get_ext_fullpath(ext.name)))

        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}/pynwn",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
        ]

        cmake_args += [
            f"-DVERSION_INFO={self.distribution.get_version()}"]

        preset = "default"  # we'll get this from OS or EVN var at some point.

        subprocess.check_call(
            ["cmake", f"--preset {preset}"] + cmake_args
        )
        subprocess.check_call(
            ["cmake", "--build", "--preset", "default"]
        )


# The information here can also be placed in setup.cfg - better separation of
# logic and declaration, and simpler if you include description/version in a file.
setup(
    name="pynwn",
    version="0.0.1",
    author="jmd",
    author_email="joshua.m.dean@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    description="libnw wrapper",
    long_description=open("README.md").read(),
    ext_modules=[CMakeExtension("src")],
    cmdclass={"build_ext": CMakeBuild},
    zip_safe=False,
    extras_require={"test": ["pytest>=6.0"]},
    python_requires=">=3.6",
)
