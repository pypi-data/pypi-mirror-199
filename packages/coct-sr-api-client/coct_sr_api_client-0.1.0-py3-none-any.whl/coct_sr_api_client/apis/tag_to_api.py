import typing_extensions

from coct_sr_api_client.apis.tags import TagValues
from coct_sr_api_client.apis.tags.service_request_group_api import ServiceRequestGroupApi
from coct_sr_api_client.apis.tags.config_group_api import ConfigGroupApi
from coct_sr_api_client.apis.tags.auth_group_api import AuthGroupApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.SERVICE_REQUEST_GROUP: ServiceRequestGroupApi,
        TagValues.CONFIG_GROUP: ConfigGroupApi,
        TagValues.AUTH_GROUP: AuthGroupApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.SERVICE_REQUEST_GROUP: ServiceRequestGroupApi,
        TagValues.CONFIG_GROUP: ConfigGroupApi,
        TagValues.AUTH_GROUP: AuthGroupApi,
    }
)
