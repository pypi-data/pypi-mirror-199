#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "tlx" for configuration "Release"
set_property(TARGET tlx APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(tlx PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libtlx.a"
  )

list(APPEND _IMPORT_CHECK_TARGETS tlx )
list(APPEND _IMPORT_CHECK_FILES_FOR_tlx "${_IMPORT_PREFIX}/lib64/libtlx.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
