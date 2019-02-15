from ..api import kongapi
__CFG = {}

service_name = "oabackend-srv"

def clear(api):
    api.delete_service(service_name)

def add(api):
    sid = api.add_service({
        "name": service_name,
        # "host":"followme-srv-oabackend-webapi.service.consul",
        "host":"192.168.8.11",
        "port":"9000",
    })
    # 根路由的接口不需要认证
    rid = api.add_route({
        "service.id": sid,
        "strip_path":"true",
        "paths[]": "/api/oabackend"
    })
     #增加oidc插件
    api.add_plugin({
        "name":"oidc",
        "route_id":rid,
        "config.client_id":"oa",
        "config.client_secret":"123456",
        "config.session_secret": "623q4hR325t36VsCD3g567922IC0073T",
        "config.redirect_uri_path":"/authenticate",
        "config.introspection_endpoint":__CFG["sso_api_addr"] + "/connect/introspect",
        "config.introspection_endpoint_auth_method": '["client_secret_basic","client_secret_post"]',
        "config.discovery":__CFG["sso_api_addr"] + "/.well-known/openid-configuration",
    })

def init(cfg):
    global __CFG
    __CFG = cfg
    api = cfg["api"]
    
    clear(api)
    add(api)

   