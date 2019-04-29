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
    # 用户凭据
    api.add_consumer({
        "username": "lagoon-client-web"
    }, {
        "type": "jwt",
        "key": "Lagoon.User",
        "algorithm": "HS256",
        "secret": "	Lagoon.User_C421AAEE0D114E9C"
    })
    

def manage_web(api):
    global _CFG
    sid = api.add_service({
        "name": "lagoon-manage-web",
        "host": __CFG["manage_web_addr"],
        "port":"10111",
    })

    rid = api.add_route({
        "service.id": sid,
        "strip_path":"false",
        "hosts[]": __CFG["manage_web_hostname"],
    })
    # 用户凭据
    api.add_consumer({
        "username": "lagoon-manage-web"
    }, {
        "type": "jwt",
        "key": "Lagoon.CRM",
        "algorithm": "HS256",
        "secret": "	Lagoon.CRM_MJ9CHCUT4NK7HFA3"
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
        "route_id":rid,
        "config.claims_to_verify":"exp"
    })
    api.add_plugin({
        "name":"jwt-claim-headers",
        "route_id":rid
    })
    api.add_route({
        "service.id": sid,
        "strip_path":"false",
        "hosts[]": __CFG["manage_web_hostname"],
        "paths[]": "/api/x-lagoon-main"
    })
    rid = api.add_route({
        "service.id": sid,
        "strip_path":"false",
        "hosts[]": __CFG["manage_web_hostname"],
        "paths[]": "/api/x-lagoon-main/manager"
    })
    api.add_plugin({
        "name":"jwt",
        "route_id":rid,
        "config.claims_to_verify":"exp"
    })
    api.add_plugin({
        "name":"jwt-claim-headers",
        "route_id":rid
    })

def clear_lagoon(api):
    api.delete_service("lagoon-main-srv")
    api.delete_service("lagoon-client-web")
    api.delete_service("lagoon-manage-web")
    api.delete_consumer("lagoon-client-web")
    api.delete_consumer("lagoon-manage-web")

def init(cfg):
    global __CFG
    __CFG = cfg
    api = cfg["api"]
    
    clear_lagoon(api)
    client_web(api)
    manage_web(api)
    main_srv(api)

    
