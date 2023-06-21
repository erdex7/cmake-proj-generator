# CMake Proj Generator

## Description

*CMake Proj Generator* is a tool for generating a project with automated CMake build.
The output generated project will include 2 subdirectories: for source code ```src``` and for unit tests ```test```:

```
ProjectName
|- CMakeLists.txt
|- src
|  |- CMakeLists.txt
|  |- main.cpp
|- test
   |- CMakeLists.txt
   |- test_case1.cpp
   |- test_case2.cpp
```

It also supports creating a project for Qt

## Usage

Just clone the repository or download the ```cmake_empty_proj.py``` file and run it:
```
python3 cmake_empty_proj.py
```
Unit testing is disabled by default. You can enable it by setting the CMake boolean option PROJ_TESTING to ON.

## Requirements

- Python 3.0 and higher;

