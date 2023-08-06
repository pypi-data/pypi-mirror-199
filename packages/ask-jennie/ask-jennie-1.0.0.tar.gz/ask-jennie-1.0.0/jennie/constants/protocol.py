KEY_EVENT_TYPE = "event_type"
KEY_FILES = "files"
KEY_LIBS = "libs"
KEY_FILE_LINK = "file_link"
KEY_OUT_PATH = "out_path"
KEY_FILE_PATH = "file_path"
KEY_SCRIPTS = "scripts"
KEY_AUTOMATIONS = "automations"
KEY_MODULE_NAME = "automations"

KEY_COMPONENTS = "components"
KEY_COMPONENT_NAME = "component_name"
KEY_COMPONENT_PATH = "component_path"
KEY_COMPONENT_FILES = "component_files"
KEY_SERVICE_NAME = "service_name"
KEY_PACKAGES = "packages"
KEY_STYLES = "styles"
KEY_IMPORTS = "imports"
KEY_PROVIDERS = "providers"
KEY_AUTH_GUARD_FILE_LINK = "auth_gaurd_file_link"
KEY_AUTH_GAURD_FILE_PATH = "auth_gaurd_file"
KEY_ROUTES_FILE_LINK = "routes_file_link"
KEY_URLS_PY_FILE_LINK = "urls_py_file_link"
KEY_SETTINGS_PY_FILE_LINK = "settings_py_file_link"
KEY_FIND_AND_REPLACE_EVENTS = "find_and_replace_events"
KEY_FIND_TEXT = "find_text"
KEY_REPLACE_TEXT = "replace_with"
KEY_MODULE_PATH = "module_path"

KEY_STACK_ANGULAR_UI_LIB = "angular-ui-lib"
KEY_STACK_ANGULAR_AUTOMATION = "angular-automations"
KEY_STACK_DJANGO_AUTOMATIONS = "django-automations"
KEY_STACK_DOCKER_AUTOMATIONS = "docker-automations"
KEY_STACK_PACKER_AUTOMATIONS = "packer-automations"
KEY_STACK_TERRAFORM_AUTOMATIONS = "terraform-automations"

KEY_LIBRARY_NAME = "library_name"
KEY_EVENT_UPLOAD = "upload"
KEY_EVENT_DOWNLOAD = "download"
KEY_EVENT_CREATE_README = "create-readme"
KEY_EVENT_UPDATE = "update"
KEY_EVENT_DELETE = "delete"
KEY_EVENT_CREATE = "create"
KEY_EVENT_ADD_EVENT = "add-event"
KEY_EVENT_SYNC = "sync"
KEY_EVENT_CREATE_API = "create-api"

EVENT_CREATE_REACTJS_COMPONENT_CLASS = "create-reactjs-component-class"
EVENT_CREATE_ANGULAR_MODULE_ROUTING = "create-angular-module-routing"
EVENT_CREATE_NAVBAR_JSON = "create-navbar-json"
EVENT_CREATE_SIDEBAR_JSON = "create-sidebar-json"
EVENT_CREATE_MULTIPLE_ANGULAR_COMPONENTS = "create-multiple-angular-components"
EVENT_CREATE_ANGULAR_MODULE = "create-angular-module"
EVENT_INSTALL_PYTHON3_LIBRARIES = "install-python3-libraries"
EVENT_ADD_SCRIPT_TO_INDEX = "add-script-to-index"
EVENT_UPDATE_SETTINGS_PY = "update-settings-py"
EVENT_REPLACE_IN_FILE = "replace-in-file"
EVENT_UPDATE_URLS_PY = "update-urls-py"
EVENT_UPDATE_ANGULAR_ROUTES = "update-angular-routes"
EVENT_UPDATE_ANGULAR_MODULES = "update-angular-modules"
EVENT_UPDATE_ANGULAR_JSON = "update-angular-json"
EVENT_INSTALL_NPM_LIBRARIES = "install-npm-libraries"
EVENT_DOWNLOAD_FILES = "download-files"
EVENT_CREATE_REACTJS_COMPONENT = "create-reactjs-component"
EVENT_DJANGO_AUTOMATIONS = "django-automations"
EVENT_CREATE_PYTHON_PACKAGE = "create-python-package"
EVENT_CREATE_ANGULAR_SERVICE = "create-angular-service"
EVENT_CREATE_ANGULAR_COMPONENT = "create-angular-component"
EVENT_COPY_ANGULAR_COMPONENT = "copy-angular-component"
EVENT_ANGULAR_UI_LIB = "angular-ui-lib"
EVENT_ANGULAR_AUTOMATIONS = "angular-automations"
EVENT_ADD_NG_LIBRARY = "add-ng-library"

UI_LIB_EVENTS = {
    KEY_EVENT_CREATE_README: None,
    KEY_EVENT_DOWNLOAD: KEY_LIBRARY_NAME,
    KEY_EVENT_UPLOAD: None,
    KEY_EVENT_UPDATE: None,
    KEY_EVENT_DELETE: KEY_LIBRARY_NAME,
    KEY_EVENT_SYNC: KEY_LIBRARY_NAME
}

AUTOMATION_EVENTS = {
    KEY_EVENT_DOWNLOAD: KEY_LIBRARY_NAME,
    KEY_EVENT_UPLOAD: None,
    KEY_EVENT_UPDATE: None,
    KEY_EVENT_DELETE: KEY_LIBRARY_NAME,
    KEY_EVENT_SYNC: None,
    KEY_EVENT_CREATE: KEY_LIBRARY_NAME,
    KEY_EVENT_ADD_EVENT: KEY_LIBRARY_NAME,
    KEY_EVENT_CREATE_README: None
}