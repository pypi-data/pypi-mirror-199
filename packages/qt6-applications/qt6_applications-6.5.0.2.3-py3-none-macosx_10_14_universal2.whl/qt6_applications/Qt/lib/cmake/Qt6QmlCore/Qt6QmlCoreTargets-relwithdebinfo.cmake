#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::QmlCore" for configuration "RelWithDebInfo"
set_property(TARGET Qt6::QmlCore APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(Qt6::QmlCore PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/QtQmlCore.framework/Versions/A/QtQmlCore"
  IMPORTED_SONAME_RELWITHDEBINFO "@rpath/QtQmlCore.framework/Versions/A/QtQmlCore"
  )

list(APPEND _cmake_import_check_targets Qt6::QmlCore )
list(APPEND _cmake_import_check_files_for_Qt6::QmlCore "${_IMPORT_PREFIX}/lib/QtQmlCore.framework/Versions/A/QtQmlCore" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
