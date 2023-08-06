from jennie.constants.protocol import *

from jennie.events.py.create_python_package import event_create_python_package
from jennie.events.py.install_python3_libraries import event_install_python3_libraries
from jennie.events.angular.create_angular_services import event_create_angular_services
from jennie.events.angular.update_angular_routes import event_update_angular_routes
from jennie.events.angular.create_angular_component import event_create_angular_component
from jennie.events.angular.copy_angular_component import event_copy_angular_component
from jennie.events.angular.angular_ui_lib import event_angular_ui_lib
from jennie.events.angular.add_ng_library import event_add_ng_library
from jennie.events.angular.create_multiple_angular_components import event_create_multiple_angular_components
from jennie.events.angular.create_angular_module import event_create_angular_module
from jennie.events.angular.create_angular_module_routing import event_create_angular_module_routing
from jennie.events.angular.update_angular_modules import event_update_angular_modules
from jennie.events.angular.update_angular_json import event_update_angular_json
from jennie.events.angular.angular_automations import event_angular_automations
from jennie.events.reactjs.create_reactjs_component import event_create_reactjs_component
from jennie.events.common.download_files import event_download_files
from jennie.events.common.replace_in_file import event_replace_in_file
from jennie.events.common.add_script_to_index import event_add_script_to_index
from jennie.events.django.update_urls_py import event_update_urls_py
from jennie.events.django.django_automations import event_django_automations
from jennie.events.django.update_settings_py import event_update_settings_py
from jennie.events.npm.install_npm_libraries import event_install_npm_libraries

ALL_EVENTS = {
    EVENT_ADD_NG_LIBRARY: event_add_ng_library,
    EVENT_ANGULAR_AUTOMATIONS: event_angular_automations,
    EVENT_ANGULAR_UI_LIB: event_angular_ui_lib,
    EVENT_COPY_ANGULAR_COMPONENT: event_copy_angular_component,
    EVENT_CREATE_ANGULAR_COMPONENT: event_create_angular_component,
    EVENT_CREATE_ANGULAR_SERVICE: event_create_angular_services,
    EVENT_CREATE_PYTHON_PACKAGE: event_create_python_package,
    EVENT_DJANGO_AUTOMATIONS: event_django_automations,
    EVENT_DOWNLOAD_FILES: event_download_files,
    EVENT_INSTALL_NPM_LIBRARIES: event_install_npm_libraries,
    EVENT_REPLACE_IN_FILE: event_replace_in_file,
    EVENT_UPDATE_ANGULAR_JSON: event_update_angular_json,
    EVENT_UPDATE_ANGULAR_MODULES: event_update_angular_modules,
    EVENT_UPDATE_ANGULAR_ROUTES: event_update_angular_routes,
    EVENT_UPDATE_SETTINGS_PY: event_update_settings_py,
    EVENT_UPDATE_URLS_PY: event_update_urls_py,
    EVENT_ADD_SCRIPT_TO_INDEX: event_add_script_to_index,
    EVENT_INSTALL_PYTHON3_LIBRARIES: event_install_python3_libraries,
}

EVENTS_ANGULAR_AUTOMATIONS = {
    EVENT_ADD_NG_LIBRARY: event_add_ng_library,
    EVENT_ANGULAR_AUTOMATIONS: event_angular_automations,
    EVENT_ANGULAR_UI_LIB: event_angular_ui_lib,
    EVENT_COPY_ANGULAR_COMPONENT: event_copy_angular_component,
    EVENT_CREATE_ANGULAR_MODULE: event_create_angular_module,
    EVENT_CREATE_ANGULAR_COMPONENT: event_create_angular_component,
    EVENT_CREATE_ANGULAR_SERVICE: event_create_angular_services,
    EVENT_DOWNLOAD_FILES: event_download_files,
    EVENT_INSTALL_NPM_LIBRARIES: event_install_npm_libraries,
    EVENT_REPLACE_IN_FILE: event_replace_in_file,
    EVENT_UPDATE_ANGULAR_JSON: event_update_angular_json,
    EVENT_UPDATE_ANGULAR_MODULES: event_update_angular_modules,
    EVENT_UPDATE_ANGULAR_ROUTES: event_update_angular_routes,
    EVENT_ADD_SCRIPT_TO_INDEX: event_add_script_to_index,
    EVENT_CREATE_MULTIPLE_ANGULAR_COMPONENTS: event_create_multiple_angular_components,
    EVENT_CREATE_ANGULAR_MODULE_ROUTING: event_create_angular_module_routing
}

EVENTS_DJANGO_AUTOMATIONS = {
    EVENT_CREATE_PYTHON_PACKAGE: event_create_python_package,
    EVENT_DJANGO_AUTOMATIONS: event_django_automations,
    EVENT_DOWNLOAD_FILES: event_download_files,
    EVENT_REPLACE_IN_FILE: event_replace_in_file,
    EVENT_UPDATE_SETTINGS_PY: event_update_settings_py,
    EVENT_UPDATE_URLS_PY: event_update_urls_py,
    EVENT_INSTALL_PYTHON3_LIBRARIES: event_install_python3_libraries,
}

EVENTS_DOCKER_AUTOMATIONS = {
    EVENT_DOWNLOAD_FILES: event_download_files
}

EVENTS_ANGULAR_UI_LIB = {
    EVENT_DOWNLOAD_FILES: event_download_files,
    EVENT_CREATE_ANGULAR_COMPONENT: event_create_angular_component,
}