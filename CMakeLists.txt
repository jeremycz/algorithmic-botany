cmake_minimum_required(VERSION 3.10)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_OSX_ARCHITECTURES "arm64")

project(AlgorithmicBotany VERSION 0.1)

add_executable(algorithmic_botany)

target_sources(algorithmic_botany PRIVATE 
               src/main.cpp
               )
