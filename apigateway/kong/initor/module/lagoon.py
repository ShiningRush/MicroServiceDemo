from ..api import kongapi
__CFG = {}

def client_web(api):
    global __CFG
    sid = api.add_service({
        "name": "lagoon-client-web",
        "host": __CFG["client_web_addr"],
        "port":"10110",
    })
    rid = api.add_route({
        "service.id": sid,
        "strip_path":"false",
        "hosts[]": __CFG["client_web_hostname"],
    })
    

def manage_web(api):
    global _CFG
    sid = api.add_service({
        "name": "lagoon-manage-web",
        "host": __CFG["manage_web_addr"],
        "port":"10111",
    })

    # 对manage的sso认证
    rid = api.add_route({
        "service.id": sid,
        "strip_path":"false",
        "hosts[]": __CFG["manage_web_hostname"],
    })
    api.add_plugin({
        "name":"oidc",
        "route_id":rid,
        "config.client_id":"lagoon_backend",
        "config.client_secret":"456123",
        "config.session_secret": "623q4hR325t36VsCD3g567922IC0073T",
        "config.redirect_uri_path":"/authenticate",
        "config.introspection_endpoint":__CFG["sso_api_addr"] + "/connect/introspect",
        "config.introspection_endpoint_auth_method": '["client_secret_basic","client_secret_post"]',
        "config.discovery":__CFG["sso_api_addr"] + "/.well-known/openid-configuration",
    })


def main_srv(api):
    global _CFG
    sid = api.add_service({
        "name": "lagoon-main-srv",
        "host":"lagoon-srv-main-webapi.service.consul",
        "port":"10101",
    })
    
    # 根路由的接口不需要认证
    rid = api.add_route({
        "service.id": sid,
        "strip_path":"false",
        "hosts[]": __CFG["client_web_hostname"],
        "paths[]": "/api/x-lagoon-main"
    })

    # 对client的jwt认证
    rid = api.add_route({
        "service.id": sid,
        "strip_path":"false",
        "hosts[]": __CFG["client_web_hostname"],
        "paths[]": "/api/x-lagoon-main/client"
    })
    api.add_plugin({
        "name":"jwt",
        "route_id":rid
    })
    api.add_plugin({
        "name":"jwt-claim-headers",
        "route_id":rid
    })

    # 对manage的sso认证
    rid = api.add_route({
        "service.id": sid,
        "strip_path":"false",
        "hosts[]": __CFG["manage_web_hostname"],
        "paths[]": "/api/x-lagoon-main/manager"
    })
    api.add_plugin({
        "name":"oidc",
        "route_id":rid,
        "config.client_id":"lagoon_backend",
        "config.client_secret":"456123",
        "config.session_secret": "623q4hR325t36VsCD3g567922IC0073T",
        "config.redirect_uri_path":"/authenticate",
        "config.introspection_endpoint":__CFG["sso_api_addr"] + "/connect/introspect",
        "config.introspection_endpoint_auth_method": '["client_secret_basic","client_secret_post"]',
        "config.discovery":__CFG["sso_api_addr"] + "/.well-known/openid-configuration",
    })

def clear_lagoon(api):
    api.delete_service("lagoon-main-srv")
    api.delete_service("lagoon-client-web")
    api.delete_service("lagoon-manage-web")
    api.delete_consumer("lagoon-client-web")

def init(cfg):
    global __CFG
    __CFG = cfg
    api = cfg["api"]
    
    clear_lagoon(api)
    client_web(api)
    manage_web(api)
    main_srv(api)

    # 用户凭据
    api.add_consumer({
        "username": "lagoon-client-web"
    }, {
        "type": "jwt",
        "key": "Lagoon.CRM",
        "algorithm": "HS256",
        "secret": "	Lagoon.CRM_C421AAEE0D114E9C"
    })

    # 通用插件用于过滤url
    api.add_plugin({
        "name": "replace-url",
        "config.replace_template": "/api/[xX]%-[a-zA-Z0-9-]*",
        "config.replace_value": ""
    })

    # CORS
    api.add_plugin({
        "name":"cors",
        "config.origins": "*"
    })
