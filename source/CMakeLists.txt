cmake_minimum_required(VERSION 2.6)

file(GLOB GENERAL RELATIVE ${CMAKE_CURRENT_SOURCE_DIR}
	[^.]*.cpp
	[^.]*.h
	[^.]*.cmake
	)

set(SOURCES ${GENERAL})

if(${T_LIB_TYPE} STREQUAL SHARED)
	add_definitions(
		-DLIBSVM_BUILD_DLL 
		-DLIBSVM_IS_DLL
	)
endif()

add_library(${PROJECT_NAME} ${T_LIB_TYPE} ${GENERAL})
