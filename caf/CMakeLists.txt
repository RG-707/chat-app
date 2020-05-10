cmake_minimum_required(VERSION 3.1.0 FATAL_ERROR)
project(chatapp_caf CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

add_custom_target(all_benchmarks ALL)
set(CAF_COMPILED_BENCHES "")

################################################################################
#                                   Utility                                    #
################################################################################

macro(add_xxx_benchmark benchname dir name src_ending bin_ending out_path)
    set(OUT_FILE ${out_path}/${name}.${bin_ending})
    set(SRC_FILE ${CMAKE_CURRENT_SOURCE_DIR}/src/${dir}/${name}.${src_ending})
    set(CAF_${benchname}_SRC_FILES ${SRC_FILE} ${CAF_${benchname}_SRC_FILES})
    set(CAF_${benchname}_${name}_OUT ${OUT_FILE})
    set(CAF_${benchname}_OUT_FILES ${OUT_FILE} ${CAF_${benchname}_OUT_FILES})
    add_custom_command(OUTPUT ${OUT_FILE}
            COMMAND ${CAF_${benchname}_COMPILER}
            ${CAF_${benchname}_COMPILER_OPTS}
            ${SRC_FILE}
            DEPENDS ${SRC_FILE} ${ARGN}
            WORKING_DIRECTORY ${EXECUTABLE_OUTPUT_PATH}
            VERBATIM)
endmacro()

# make files show up in GUI even if not building a particular benchmark
macro(add_dummy_target benchname src_ending)
    # check all aditional dependency flags
    set(globstr "${CMAKE_CURRENT_SOURCE_DIR}/src/${benchname}/*.${src_ending}")
    foreach(additional_ending ${ARGN})
        set(globstr ${globstr}
                "${CMAKE_CURRENT_SOURCE_DIR}/src/${benchname}/*.${additional_ending}")
    endforeach()
    file(GLOB_RECURSE source_files ${globstr})
    add_custom_target(caf_${benchname}_dummy SOURCES ${source_files})
endmacro()

################################################################################
#                                     CAF                                      #
################################################################################
set(CMAKE_CXX_STANDARD 11)
# check if the user provided CXXFLAGS, set defaults otherwise
if(NOT CMAKE_CXX_FLAGS)
    set(CMAKE_CXX_FLAGS                   "-std=c++11 -Wextra -Wall -pedantic -pthread")
endif()
if (NOT MSVC AND NOT "${CMAKE_CXX_FLAGS}" MATCHES "-std=")
    message(STATUS "Supplied CXXFLAGS do not contain a C++ standard, setting std to c++11")
    set(CMAKE_CXX_FLAGS                   "-std=c++11 ${CMAKE_CXX_FLAGS}")
endif()
if(NOT CMAKE_CXX_FLAGS_DEBUG)
    set(CMAKE_CXX_FLAGS_DEBUG             "-O0 -g")
endif()
if(NOT CMAKE_CXX_FLAGS_MINSIZEREL)
    set(CMAKE_CXX_FLAGS_MINSIZEREL        "-Os")
endif()
if(NOT CMAKE_CXX_FLAGS_RELEASE)
    set(CMAKE_CXX_FLAGS_RELEASE           "-O3 -DNDEBUG")
endif()
if(NOT CMAKE_CXX_FLAGS_RELWITHDEBINFO)
    set(CMAKE_CXX_FLAGS_RELWITHDEBINFO    "-O2 -g -fno-omit-frame-pointer")
endif()
# set build default build type to RelWithDebInfo if not set
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE RelWithDebInfo)
endif()
find_package(CAF COMPONENTS core io REQUIRED)
add_custom_target(caf_benchmarks)
message(STATUS "CAF_INCLUDES: ${CAF_INCLUDE_DIRS}")
include_directories(${CAF_INCLUDE_DIRS})
# add targets for CAF benchmarks
add_executable(caf ${CMAKE_CURRENT_SOURCE_DIR}/src/chatapp.cpp)
target_link_libraries(caf ${CAF_LIBRARIES} ${LD_FLAGS})
add_dependencies(caf_benchmarks caf)
add_dependencies(all_benchmarks caf_benchmarks)
set(CAF_COMPILED_BENCHES "caf ${CAF_COMPILED_BENCHES}")
