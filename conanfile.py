from conans import ConanFile, CMake, tools
import os
import shutil

class ArmadilloConan(ConanFile):
    name = "armadillo"
    version = "9.700.3"
    license = "Apache License 2.0"
    url = "http://arma.sourceforge.net/"
    description = "Armadillo is a high quality linear algebra library (matrix maths) for the C++ language, aiming towards a good balance between speed and ease of use"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "arma_use_lapack" : [True, False],
        "arma_use_blas" : [True, False]
        }
    default_options = {
        "arma_use_lapack": True,
        "arma_use_blas": True 
        }
    generators = "cmake"
    requires = ("lapack/3.7.1@kang/stable")
    
    def configure(self):
        if self.settings.compiler == "Visual Studio":
            self.options["lapack"].visual_studio = True
            self.options["lapack"].shared = True

    def source(self):
        zip_name = "armadillo-%s.tar.xz" % self.version
        folder_name = "armadillo-%s" % self.version
        tools.download("https://iweb.dl.sourceforge.net/project/arma/" + zip_name, filename=zip_name)
        tools.untargz(zip_name)
        os.unlink(zip_name)
        shutil.move(folder_name, "armadillo")

        if not self.options.arma_use_lapack:
            tools.replace_in_file(file_path="armadillo/include/armadillo_bits/config.hpp",
                                  search="#define arma_use_lapack",
                                  replace="//#define arma_use_lapack")
        if not self.options.arma_use_blas:
            tools.replace_in_file(file_path="armadillo/include/armadillo_bits/config.hpp",
                                  search="#define arma_use_blas",
                                  replace="//#define arma_use_blas")
        
    def build(self):
        cmake = CMake(self)
        cmake.configure(build_dir="build", source_dir="../armadillo")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("armadillo_bits/*", dst="include", src="armadillo/include")
        self.copy("armadillo", dst="include", src="armadillo/include")
        self.copy("*.lib", dst="lib", src="build", keep_path=False)
        self.copy("*.dll", dst="bin", src="build", keep_path=False)
        self.copy("*.so", dst="lib", src="build", keep_path=False)
        self.copy("*.dylib", dst="lib", src="build", keep_path=False)
        self.copy("*.a", dst="lib", src="build", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["armadillo"]

