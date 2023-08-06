#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt6::QDarwinCalendarPermissionPlugin" for configuration "RelWithDebInfo"
set_property(TARGET Qt6::QDarwinCalendarPermissionPlugin APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(Qt6::QDarwinCalendarPermissionPlugin PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELWITHDEBINFO "CXX;OBJCXX"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/./plugins/permissions/libqdarwincalendarpermission.a"
  )

list(APPEND _cmake_import_check_targets Qt6::QDarwinCalendarPermissionPlugin )
list(APPEND _cmake_import_check_files_for_Qt6::QDarwinCalendarPermissionPlugin "${_IMPORT_PREFIX}/./plugins/permissions/libqdarwincalendarpermission.a" )

# Import target "Qt6::QDarwinCalendarPermissionPlugin_init" for configuration "RelWithDebInfo"
set_property(TARGET Qt6::QDarwinCalendarPermissionPlugin_init APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(Qt6::QDarwinCalendarPermissionPlugin_init PROPERTIES
  IMPORTED_COMMON_LANGUAGE_RUNTIME_RELWITHDEBINFO ""
  IMPORTED_OBJECTS_RELWITHDEBINFO "${_IMPORT_PREFIX}/./plugins/permissions/objects-RelWithDebInfo/QDarwinCalendarPermissionPlugin_init/QDarwinCalendarPermissionPlugin_init.cpp.o"
  )

list(APPEND _cmake_import_check_targets Qt6::QDarwinCalendarPermissionPlugin_init )
list(APPEND _cmake_import_check_files_for_Qt6::QDarwinCalendarPermissionPlugin_init "${_IMPORT_PREFIX}/./plugins/permissions/objects-RelWithDebInfo/QDarwinCalendarPermissionPlugin_init/QDarwinCalendarPermissionPlugin_init.cpp.o" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
