#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::QuickDialogs2Utils" for configuration "RelWithDebInfo"
set_property(TARGET Qt6::QuickDialogs2Utils APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(Qt6::QuickDialogs2Utils PROPERTIES
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/QtQuickDialogs2Utils.framework/Versions/A/QtQuickDialogs2Utils"
  IMPORTED_SONAME_RELWITHDEBINFO "@rpath/QtQuickDialogs2Utils.framework/Versions/A/QtQuickDialogs2Utils"
  )

list(APPEND _cmake_import_check_targets Qt6::QuickDialogs2Utils )
list(APPEND _cmake_import_check_files_for_Qt6::QuickDialogs2Utils "${_IMPORT_PREFIX}/lib/QtQuickDialogs2Utils.framework/Versions/A/QtQuickDialogs2Utils" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
