#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::qtquickcontrols2iosstyleplugin" for configuration "RelWithDebInfo"
set_property(TARGET Qt6::qtquickcontrols2iosstyleplugin APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(Qt6::qtquickcontrols2iosstyleplugin PROPERTIES
  IMPORTED_COMMON_LANGUAGE_RUNTIME_RELWITHDEBINFO ""
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/./qml/QtQuick/Controls/iOS/libqtquickcontrols2iosstyleplugin.dylib"
  IMPORTED_NO_SONAME_RELWITHDEBINFO "TRUE"
  )

list(APPEND _cmake_import_check_targets Qt6::qtquickcontrols2iosstyleplugin )
list(APPEND _cmake_import_check_files_for_Qt6::qtquickcontrols2iosstyleplugin "${_IMPORT_PREFIX}/./qml/QtQuick/Controls/iOS/libqtquickcontrols2iosstyleplugin.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
