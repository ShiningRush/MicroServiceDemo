from ..api import kongapi

def init(api_addr):
    api = kongapi.KongApi(api_addr)

    sid = api.add_service({
        "name": "testservice",
        "host":"testjwt.com",
        "port":"56000",
    })
    print(sid)
    
    rid = api.add_route({
        "service.id": sid,
        "hosts[]": "foo.com",
        "strip_path":"false",
    })
    print(rid)

    cid = api.add_consumer({
        "username": "lagoon-client-web"
    }, {
        "type": "jwt",
        "algorithm": "HS256",
        "secret": "	Lagoon.CRM_C421AAEE0D114E9C"
    })
    print(cid)

    pid = api.add_plugin({
        "name":"jwt",
        "route_id":rid
    })
    print(pid)    