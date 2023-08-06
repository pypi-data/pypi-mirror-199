# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from coct_sr_api_client.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    SERVICE_REQUEST_GROUP = "service_request_group"
    CONFIG_GROUP = "config_group"
    AUTH_GROUP = "auth_group"
