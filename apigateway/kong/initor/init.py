from .module import lagoon
from .api import kongapi

def init(env):
    if env == "dev":
        from . import dev as cfg
    
    if env == "beta":
        from . import beta as cfg
    
    if env == "pro":
        from . import pro as cfg

    c = cfg.config()
    api = kongapi.KongApi(c["kong_api_addr"])
    c["api"] = api
    
    lagoon.init(c)