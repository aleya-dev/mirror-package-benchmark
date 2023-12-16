from conan import ConanFile
from conan.tools.cmake import CMakeToolchain
from conan.tools.files import rmdir
import os


required_conan_version = ">=2.0"


class BenchmarkConan(ConanFile):
    name = "benchmark"
    version = "1.8.3"
    python_requires = "aleya-conan-base/1.3.0@aleya/public"
    python_requires_extend = "aleya-conan-base.AleyaCmakeBase"

    exports_sources = "source/*"

    options = {
        "shared": [False],
        "fPIC": [False, True]
    }

    default_options = {
        "shared": False,
        "fPIC": True
    }

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_SHARED_LIBS"] = False
        tc.variables["BENCHMARK_ENABLE_ASSEMBLY_TESTS"] = False
        tc.variables["BENCHMARK_DOWNLOAD_DEPENDENCIES"] = False
        tc.variables["BENCHMARK_ENABLE_DOXYGEN"] = False
        tc.variables["BENCHMARK_ENABLE_GTEST_TESTS"] = False
        tc.variables["BENCHMARK_USE_BUNDLED_GTEST"] = False
        tc.variables["BENCHMARK_ENABLE_TESTING"] = False
        tc.variables["BENCHMARK_ENABLE_INSTALL"] = True
        tc.variables["BENCHMARK_INSTALL_DOCS"] = False
        tc.generate()

    def package(self):
        super().package()

        rmdir(self, os.path.join(self.package_folder, "bin"))
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "benchmark")

        self.cpp_info.components["_benchmark"].libs = ["benchmark"]
        self.cpp_info.components["_benchmark"].set_property("cmake_target_name", "benchmark::benchmark")
        self.cpp_info.components["_benchmark"].defines.append("BENCHMARK_STATIC_DEFINE")

        if self.settings.os in ("FreeBSD", "Linux"):
            self.cpp_info.components["_benchmark"].system_libs.extend(["pthread", "rt", "m"])
        elif self.settings.os == "Windows":
            self.cpp_info.components["_benchmark"].system_libs.append("shlwapi")

        self.cpp_info.components["benchmark_main"].set_property("cmake_target_name", "benchmark::benchmark_main")
        self.cpp_info.components["benchmark_main"].libs = ["benchmark_main"]
        self.cpp_info.components["benchmark_main"].requires = ["_benchmark"]
