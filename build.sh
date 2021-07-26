#!/bin/sh

if [ ! -d "/path/to/dir" ] 
then
    mkdir build 
fi

cd build

cmake -G Xcode ..
cmake --build .