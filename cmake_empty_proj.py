import os
import re

class ProjValues:
    project_name = "NoName"
    project_version = "1.0"
    cmake_min_version = "3.14" # Set the minimum version of CMake that can be used
    source_dir_name = "src"
    tests_dir_name = "test"
    tests_file_name = ["test_case1", "test_case2"]
    using_qt = False

proj_values = ProjValues()    

def createFile(path, name, body):
    file_obj = open(path + "/" + name, "w+")
    file_obj.write(body)
    file_obj.close()

def getInput(text, condition):
    while True:
        res = input(text)
        if not res:
            return ""
        if condition(res):
            return res
        print("Error setting the value, try again...")

def initProjValues():
    global proj_values

    res = getInput("Minimum required CMake version (by default 3.14): ", 
                    lambda val: re.search("^(([0-9]+)\\.){0,2}([0-9]+)$", val))
    if res:
        proj_values.cmake_min_version = res

    res = getInput("Project name: ", lambda val: not " " in val)
    if res:
        proj_values.project_name = res

    res = getInput("Is this project using Qt (y/n) (by default No): ", 
                    lambda val: val.capitalize() == 'Y' or val.capitalize() == 'N')
    proj_values.using_qt = res.capitalize() == 'Y'       

def main():
    initProjValues()

    # Create directory
    path_to_proj_root = os.path.dirname(__file__) + "/" + proj_values.project_name
    path_to_src = path_to_proj_root + "/" + proj_values.source_dir_name
    path_to_test = path_to_proj_root + "/" + proj_values.tests_dir_name
    os.makedirs(path_to_src)
    os.makedirs(path_to_test)

    # Create template files
    mainFileBody = ("#include <iostream>\n\n"
                    "int main(int argc, char* argv[])\n"
                    "{\n\tstd::cout << \"Hello World!\\n\";"
                    "\n\treturn 0;\n}")
    createFile(path_to_src, "main.cpp", mainFileBody)

    for i in [0, 1]:
        createFile(path_to_test, proj_values.tests_file_name[i] + ".cpp", "")

    # Create CMakeFiles
    createFile(path_to_proj_root, "CMakeLists.txt", generateRootCMakeBody())
    createFile(path_to_src, "CMakeLists.txt", generateSrcCMakeBody())
    createFile(path_to_test, "CMakeLists.txt", generateTestsCMakeBody())

def generateRootCMakeBody():
    res = ( "cmake_minimum_required (VERSION " + proj_values.cmake_min_version + ")\n\n"
            "project (" + proj_values.project_name +
            " VERSION " + proj_values.project_version +
            " LANGUAGES CXX)\n\n"
            "option(PROJ_TESTING \"Enable unit tests\" OFF)\n\n"
            "if((CMAKE_CXX_COMPILER_ID MATCHES \"GNU\") OR (CMAKE_CXX_COMPILER_ID MATCHES \"Clang\"))\n"
            "    add_compile_options(\n"
            "        -Wall\n"
            "        -Wextra\n"
            "        -Wpedantic\n"
            "        -Wcast-align\n"
            "        -Wcast-qual\n"
            "        -Wconversion\n"
            "        -Wctor-dtor-privacy\n"
            "        -Wenum-compare\n"
            "        -Wfloat-equal\n"
            "        -Wnon-virtual-dtor\n"
            "        -Wold-style-cast\n"
            "        -Woverloaded-virtual\n"
            "        -Wredundant-decls\n"
            "        -Wsign-conversion\n"
            "        -Wsign-promo\n"
            "        -Wshadow\n"
            "    )\n"
            "elseif(CMAKE_CXX_COMPILER_ID MATCHES \"MSVC\")\n"
            "    add_compile_options(/W4 /WX)\n"
            "endif()\n\n"
            "add_subdirectory (" + proj_values.source_dir_name + ")\n\n"
            "if (PROJ_TESTING)\n"
            "    add_subdirectory (" + proj_values.tests_dir_name + ")\n"
            "else()\n"
            "    message(STATUS \"Testing project is turned off\")\n"
            "endif()")
    return res

def generateSrcCMakeBody():
    res = ""
    if proj_values.using_qt:
        res += "set(CMAKE_AUTOUIC ON)\n"
        res += "set(CMAKE_AUTOMOC ON)\n"
        res += "set(CMAKE_AUTORCC ON)\n\n"

    res += "set(CMAKE_CXX_STANDARD 17)\n"
    res += "set(CMAKE_CXX_STANDARD_REQUIRED ON)\n\n"

    if proj_values.using_qt:
        res += "find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Core)\n"
        res += "find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Core)\n\n"

    
    res += "set(SOURCE_APP\n    main.cpp\n)\n\n"


    res += "add_executable(" + proj_values.project_name + " ${SOURCE_APP})\n\n"

    if proj_values.using_qt:
        res += "target_link_libraries(" + proj_values.project_name + " PRIVATE Qt${QT_VERSION_MAJOR}::Core)\n"
    return res

def generateTestsCMakeBody():
    res = "project (" + proj_values.project_name + "_test)\n"
    res += "enable_testing()\n\n"
    if proj_values.using_qt:
        res += "find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Test)\n"
        res += "find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Test)\n\n"
        res += "set(CMAKE_AUTOUIC ON)\n"
        res += "set(CMAKE_AUTOMOC ON)\n"
        res += "set(CMAKE_AUTORCC ON)\n\n"
    
    res += "set(CMAKE_CXX_STANDARD 17)\n"
    res += "set(CMAKE_CXX_STANDARD_REQUIRED ON)\n\n"

    for i in [0, 1]:        
        test_name = proj_values.tests_file_name[i]
        res += "add_executable({} {}.cpp)\n".format(test_name, test_name)
        res += "add_test(NAME {} COMMAND {})\n".format(test_name, test_name)
        if proj_values.using_qt:
            res += "target_link_libraries({} PRIVATE Qt${{QT_VERSION_MAJOR}}::Test)\n\n".format(test_name)
        else:
            res += "#target_link_libraries({} PRIVATE ) # Link your test library\n\n".format(test_name)
    return res

if __name__=="__main__":
    main()
