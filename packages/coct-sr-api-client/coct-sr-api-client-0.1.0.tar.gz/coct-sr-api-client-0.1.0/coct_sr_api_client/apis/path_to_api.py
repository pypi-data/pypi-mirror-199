import typing_extensions

from coct_sr_api_client.paths import PathValues
from coct_sr_api_client.apis.paths.zcur_guest_login import ZcurGuestLogin
from coct_sr_api_client.apis.paths.zsreq_session import ZsreqSession
from coct_sr_api_client.apis.paths.zsreq_config_types import ZsreqConfigTypes
from coct_sr_api_client.apis.paths.zsreq_config_subtypes import ZsreqConfigSubtypes
from coct_sr_api_client.apis.paths.zsreq_sr_reference_no import ZsreqSrReferenceNo
from coct_sr_api_client.apis.paths.zsreq_sr import ZsreqSr

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.ZCURGUEST_LOGIN: ZcurGuestLogin,
        PathValues.ZSREQ_SESSION: ZsreqSession,
        PathValues.ZSREQ_CONFIG_TYPES: ZsreqConfigTypes,
        PathValues.ZSREQ_CONFIG_SUBTYPES: ZsreqConfigSubtypes,
        PathValues.ZSREQ_SR_REFERENCE_NO: ZsreqSrReferenceNo,
        PathValues.ZSREQ_SR: ZsreqSr,
    }
)

path_to_api = PathToApi(
    {
        PathValues.ZCURGUEST_LOGIN: ZcurGuestLogin,
        PathValues.ZSREQ_SESSION: ZsreqSession,
        PathValues.ZSREQ_CONFIG_TYPES: ZsreqConfigTypes,
        PathValues.ZSREQ_CONFIG_SUBTYPES: ZsreqConfigSubtypes,
        PathValues.ZSREQ_SR_REFERENCE_NO: ZsreqSrReferenceNo,
        PathValues.ZSREQ_SR: ZsreqSr,
    }
)
