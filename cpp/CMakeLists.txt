cmake_minimum_required(VERSION 3.16)
project(five_senses_prompt LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(example_usage example_usage.cpp)
target_include_directories(example_usage PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# Header-only library target for consumers who just want the prompt constant.
add_library(five_senses_prompt INTERFACE)
target_include_directories(five_senses_prompt INTERFACE ${CMAKE_CURRENT_SOURCE_DIR})
target_compile_features(five_senses_prompt INTERFACE cxx_std_20)
