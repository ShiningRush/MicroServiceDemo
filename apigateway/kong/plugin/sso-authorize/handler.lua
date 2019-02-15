local http = require "resty.http"
local responses = require "kong.tools.responses"
local cjson = require "cjson.safe"

-- load the base plugin object and create a subclass
local plugin = require("kong.plugins.base_plugin"):extend()

-- constructor
function plugin:new()
  plugin.super.new(self, "sso-authorize")
  
  -- do initialization here, runs in the 'init_by_lua_block', before worker processes are forked

end

---------------------------------------------------------------------------------------------
-- In the code below, just remove the opening brackets; `[[` to enable a specific handler
--
-- The handlers are based on the OpenResty handlers, see the OpenResty docs for details
-- on when exactly they are invoked and what limitations each handler has.
--
-- The call to `.super.xxx(self)` is a call to the base_plugin, which does nothing, except logging
-- that the specific handler was executed.
---------------------------------------------------------------------------------------------


--[[ handles more initialization, but AFTER the worker process has been forked/created.
-- It runs in the 'init_worker_by_lua_block'
function plugin:init_worker()
  plugin.super.access(self)

  -- your custom code here
  
end --]]

--[[ runs in the ssl_certificate_by_lua_block handler
function plugin:certificate(plugin_conf)
  plugin.super.access(self)

  -- your custom code here
  
end --]]

--[[ runs in the 'rewrite_by_lua_block' (from version 0.10.2+)
-- IMPORTANT: during the `rewrite` phase neither the `api` nor the `consumer` will have
-- been identified, hence this handler will only be executed if the plugin is 
-- configured as a global plugin!
function plugin:rewrite(plugin_conf)
  plugin.super.rewrite(self)

  -- your custom code here
  
end --]]

---[[ runs in the 'access_by_lua_block'
function plugin:access(plugin_conf)
  plugin.super.access(self)
  
  local httpc = http.new()

  local hs = ngx.req.get_headers()  

  kong.log.debug("request path:"..kong.request.get_path())
  kong.log.debug("nginx matched uri:"..ngx.ctx.router_matches.uri)
  kong.log.debug("nginx upstream_url:"..ngx.var.upstream_uri)
  
  local post_body = cjson.encode({
      accessToken = hs["X-Access-Token"],
      applicationId = plugin_conf.client_id,
      permissionName = ngx.var.upstream_uri,
    })
  kong.log.debug("body"..post_body)
  local res, err = httpc:request_uri(plugin_conf.authorize_endpoint.."/auth/PermissionEnable", { 
    method = "POST",
    body    = post_body,
    headers = {
      ["Content-Type"]  = "application/json"
    }
  })
  if not res then
    return responses.send_HTTP_INTERNAL_SERVER_ERROR(err)
  end
  kong.log.debug("response:"..res.body)
  local resp = cjson.decode(res.body)
  if not resp.enable then
    kong.log.debug("authorize failed:"..resp.message)
    ngx.status = ngx.HTTP_UNAUTHORIZED
    ngx.say("SSO UnAuthorized: You have no permission to access this method")
    ngx.exit(ngx.HTTP_UNAUTHORIZED)
  end
end --]]

---[[ runs in the 'header_filter_by_lua_block'
function plugin:header_filter(plugin_conf)
  plugin.super.access(self)

  -- your custom code here, for example;
end --]]

--[[ runs in the 'body_filter_by_lua_block'
function plugin:body_filter(plugin_conf)
  plugin.super.access(self)

  -- your custom code here
  
end --]]

--[[ runs in the 'log_by_lua_block'
function plugin:log(plugin_conf)
  plugin.super.access(self)

  -- your custom code here
  
end --]]


-- set the plugin priority, which determines plugin execution order
plugin.PRIORITY = -2

-- return our plugin object
return plugin
