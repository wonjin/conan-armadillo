project(PackageTest CXX)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(example example.cpp)
target_link_libraries(example ${CONAN_LIBS})
# list(REMOVE_ITEM CONAN_LIBS ${CONAN_LIBS_LAPACK})
# target_link_libraries(example ${CONAN_LIBS} liblapack libblas)