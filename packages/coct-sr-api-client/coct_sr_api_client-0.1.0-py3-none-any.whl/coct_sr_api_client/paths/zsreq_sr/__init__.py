# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from coct_sr_api_client.paths.zsreq_sr import Api

from coct_sr_api_client.paths import PathValues

path = PathValues.ZSREQ_SR