cmake_minimum_required(VERSION 2.6)

project(Libsvm-Practice)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${T_OUTPUT_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${T_OUTPUT_DIR})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${T_OUTPUT_DIR})

if(${T_BUILD_LIBTYPE} STREQUAL static)
  set(T_LIB_TYPE STATIC)
else()
  set(T_LIB_TYPE SHARED)
endif()

include_directories(external/libsvm)
include_directories(source)

add_subdirectory(source)