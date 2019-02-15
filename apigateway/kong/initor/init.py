from .api import kongapi
from .module import lagoon
from .module import contentmanage
from .module import common
from .module import oabackend


def init(env, module):
    if env == "dev":
        from . import dev as cfg
    
    if env == "beta":
        from . import beta as cfg
    
    if env == "pro":
        from . import pro as cfg

    c = cfg.config()
    api = kongapi.KongApi(c["kong_api_addr"])
    c["api"] = api
    
    modules = {
        'lagoon': lagoon.init,
        'contentmanage': contentmanage.init,
        'common': common.init,
        'oabackend': oabackend.init
    }

    modules[module](c)
