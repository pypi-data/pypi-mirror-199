#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::QuickDialogs2" for configuration "RelWithDebInfo"
set_property(TARGET Qt6::QuickDialogs2 APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(Qt6::QuickDialogs2 PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELWITHDEBINFO "Qt6::QuickControls2Impl;Qt6::QuickDialogs2Utils;Qt6::QuickDialogs2QuickImpl;Qt6::Qml"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/QtQuickDialogs2.framework/Versions/A/QtQuickDialogs2"
  IMPORTED_SONAME_RELWITHDEBINFO "@rpath/QtQuickDialogs2.framework/Versions/A/QtQuickDialogs2"
  )

list(APPEND _cmake_import_check_targets Qt6::QuickDialogs2 )
list(APPEND _cmake_import_check_files_for_Qt6::QuickDialogs2 "${_IMPORT_PREFIX}/lib/QtQuickDialogs2.framework/Versions/A/QtQuickDialogs2" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
