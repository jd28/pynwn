from setuptools import find_packages
import os
import subprocess
import sys

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext


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

        preset = "default"
        debug = int(os.environ.get("DEBUG", 0)
                    ) if self.debug is None else self.debug
        cfg = "Debug" if debug else "Release"

        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}/pynwn",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            f"-DCMAKE_BUILD_TYPE={cfg}",  # not used on MSVC, but no harm
            f"-DVERSION_INFO={self.distribution.get_version()}",
        ]

        if self.compiler.compiler_type == "msvc":
            cmake_args += [
                f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{cfg.upper()}={extdir}"
            ]
            preset = "windows-default"
        elif self.plat_name.startswith("macosx"):
            preset = "macos-default"
        elif os.environ.get('CIBUILDWHEEL', '0') == '1':
            preset = "ci-default"

        subprocess.check_call(
            ["cmake", f"--preset {preset}"] + cmake_args
        )
        subprocess.check_call(
            ["cmake", "--build", "--preset", "default"]
        )


setup(
    name="pynwn",
    version="0.1.0",
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
    python_requires=">=3.8",
)
