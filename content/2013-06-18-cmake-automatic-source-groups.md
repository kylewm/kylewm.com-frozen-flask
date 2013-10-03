---
category = "Programming"
layout = "post"
title = "Automatic CMake source groups based on folders"
abstract = "Using CMake to generate a Visual Studio project, create folders based on the actual directory structure."
tags = [ "cmake",]
date = 2013-06-18T00:00:00Z
---


Using CMake to generate a Visual Studio project, it is nice for the VS
folders to mirror the folder structure of your project.  The following
snippet loops through a list of files and adds them to source groups
based on their relative path.

    :::cmake
    set(ALL_FILES
      src/SomeClass.cpp
      include/SomeClass.h
      ...)

    add_library(MyLibrary ${ALL_FILES})

    foreach(FILE ${ALL_FILES}) 
      get_filename_component(PARENT_DIR "${FILE}" PATH)

      # skip src or include and changes /'s to \\'s
      string(REGEX REPLACE "(\\./)?(src|include)/?" "" GROUP "${PARENT_DIR}")
      string(REPLACE "/" "\\" GROUP "${GROUP}")

      # group into "Source Files" and "Header Files"
      if ("${FILE}" MATCHES ".*\\.cpp")
        set(GROUP "Source Files\\${GROUP}")
      elseif("${FILE}" MATCHES ".*\\.h")
        set(GROUP "Header Files\\${GROUP}")
      endif()

      source_group("${GROUP}" FILES "${FILE}")
    endforeach()
