#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::QuickControls2" for configuration "RelWithDebInfo"
set_property(TARGET Qt6::QuickControls2 APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(Qt6::QuickControls2 PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELWITHDEBINFO "Qt6::QuickTemplates2;Qt6::Qml"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/QtQuickControls2.framework/Versions/A/QtQuickControls2"
  IMPORTED_SONAME_RELWITHDEBINFO "@rpath/QtQuickControls2.framework/Versions/A/QtQuickControls2"
  )

list(APPEND _cmake_import_check_targets Qt6::QuickControls2 )
list(APPEND _cmake_import_check_files_for_Qt6::QuickControls2 "${_IMPORT_PREFIX}/lib/QtQuickControls2.framework/Versions/A/QtQuickControls2" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
