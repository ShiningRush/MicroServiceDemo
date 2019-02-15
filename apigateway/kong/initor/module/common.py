def init(cfg):
    api = cfg["api"]

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