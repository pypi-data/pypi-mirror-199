# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from coct_sr_api_client.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    ZCURGUEST_LOGIN = "/zcur-guest/login"
    ZSREQ_SESSION = "/zsreq/session"
    ZSREQ_CONFIG_TYPES = "/zsreq/config/types"
    ZSREQ_CONFIG_SUBTYPES = "/zsreq/config/subtypes"
    ZSREQ_SR_REFERENCE_NO = "/zsreq/sr/{reference_no}"
    ZSREQ_SR = "/zsreq/sr"
