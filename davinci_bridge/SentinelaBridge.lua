-- SentinelaBridge v1
-- Ponte persistente e generica entre Codex/Sentinela e Lua dentro do DaVinci Resolve.
-- O bridge apenas transporta requisicoes e carrega modulos Lua locais por nome.
-- Nao aceita codigo em texto, caminhos arbitrarios, shell ou sockets.

local SEP = package.config:sub(1, 1)

local home = os.getenv("SENTINELA_BRIDGE_HOME")
if not home or home == "" then
    local user = os.getenv("USERPROFILE") or os.getenv("HOME") or "."
    home = user .. SEP .. "SentinelaBridge"
end

local modules_home = os.getenv("SENTINELA_BRIDGE_MODULES")
if not modules_home or modules_home == "" then
    modules_home = home .. SEP .. "modules"
end

local inbox = home .. SEP .. "inbox"
local outbox = home .. SEP .. "outbox"
local logs = home .. SEP .. "logs"
local request_path = inbox .. SEP .. "request.txt"
local response_path = outbox .. SEP .. "response.txt"
local last_id_path = home .. SEP .. "last_id.txt"
local log_path = logs .. SEP .. "bridge.log"

local function mkdir(path)
    if bmd and bmd.direxists and bmd.createdir then
        if not bmd.direxists(path) then bmd.createdir(path) end
    end
end

mkdir(home)
mkdir(inbox)
mkdir(outbox)
mkdir(logs)
mkdir(modules_home)

local function read_file(path)
    local f = io.open(path, "r")
    if not f then return nil end
    local data = f:read("*a")
    f:close()
    return data
end

local function write_file(path, data)
    local tmp = path .. ".tmp"
    local f, err = io.open(tmp, "w")
    if not f then return false, err end
    f:write(data)
    f:close()
    os.remove(path)
    local ok, rename_err = os.rename(tmp, path)
    if not ok then return false, rename_err end
    return true
end

local function clean(v)
    v = tostring(v or "")
    return (v:gsub("[\r\n]", " "))
end

local function append_log(line)
    local f = io.open(log_path, "a")
    if f then
        f:write(os.date("!%Y-%m-%dT%H:%M:%SZ") .. " " .. clean(line) .. "\n")
        f:close()
    end
end

local function parse_kv(text)
    local t = {}
    for line in tostring(text):gmatch("[^\r\n]+") do
        local k, v = line:match("^([%w_%.%-]+)%s*=%s*(.*)$")
        if k then t[k] = v end
    end
    return t
end

local function encode_kv(t)
    local keys = {}
    for k in pairs(t) do keys[#keys + 1] = k end
    table.sort(keys)
    local lines = {}
    for _, k in ipairs(keys) do
        lines[#lines + 1] = clean(k) .. "=" .. clean(t[k])
    end
    return table.concat(lines, "\n") .. "\n"
end

local function get_resolve()
    if resolve then return resolve end
    if bmd and bmd.scriptapp then return bmd.scriptapp("Resolve") end
    return nil
end

local function snapshot(r)
    local result = {
        status = "ok",
        product = r.GetProductName and r:GetProductName() or "DaVinci Resolve",
        version = r.GetVersionString and r:GetVersionString() or "unknown",
        page = r.GetCurrentPage and (r:GetCurrentPage() or "") or "",
    }

    local pm = r.GetProjectManager and r:GetProjectManager() or nil
    local project = pm and pm:GetCurrentProject() or nil
    if project then
        result.project = project:GetName() or ""
        local timeline = project:GetCurrentTimeline()
        if timeline then
            result.timeline = timeline:GetName() or ""
            if timeline.GetTrackCount then
                result.video_tracks = timeline:GetTrackCount("video") or 0
                result.audio_tracks = timeline:GetTrackCount("audio") or 0
            end
        else
            result.timeline = ""
        end
    else
        result.project = ""
        result.timeline = ""
    end
    return result
end

local function valid_module_name(name)
    return type(name) == "string" and name ~= "" and name:match("^[%w_%-]+$") ~= nil
end

local function load_module(name)
    if not valid_module_name(name) then
        return nil, "invalid_module_name"
    end

    local path = modules_home .. SEP .. name .. ".lua"
    local chunk, load_err = loadfile(path)
    if not chunk then
        return nil, "module_load_failed: " .. clean(load_err)
    end

    local ok, exported = pcall(chunk)
    if not ok then
        return nil, "module_init_failed: " .. clean(exported)
    end

    if type(exported) == "function" then
        return exported, nil
    end
    if type(exported) == "table" and type(exported.run) == "function" then
        return exported.run, nil
    end
    return nil, "module_must_return_function_or_table_with_run"
end

local function run_module(r, req)
    local name = req.module or ""
    local runner, err = load_module(name)
    if not runner then
        return { status="error", error=err, module=name }
    end

    local ctx = {
        resolve = r,
        bridge_home = home,
        modules_home = modules_home,
        snapshot = snapshot,
        log = append_log,
    }

    local ok, result = pcall(runner, ctx, req)
    if not ok then
        return { status="error", error="module_exception", detail=clean(result), module=name }
    end
    if type(result) ~= "table" then
        return { status="error", error="module_result_must_be_table", module=name }
    end
    if result.status == nil then result.status = "ok" end
    result.module = name
    return result
end

local function execute(req)
    local r = get_resolve()
    if not r then
        return { id=req.id or "", status="error", error="resolve_unavailable" }
    end

    local cmd = string.upper(req.command or "PING")
    local result

    if cmd == "PING" then
        result = snapshot(r)
        result.bridge = "SentinelaBridge-v1"
        result.modules_home = modules_home

    elseif cmd == "RUN" then
        result = run_module(r, req)

    elseif cmd == "STOP_BRIDGE" then
        result = snapshot(r)
        result.stop = "true"

    else
        result = { status="error", error="unsupported_bridge_command", command=cmd }
    end

    result.id = req.id or ""
    result.command = cmd
    return result
end

append_log("START v1 home=" .. home .. " modules=" .. modules_home)
print("[SentinelaBridge] v1 ativo em: " .. home)
print("[SentinelaBridge] modulos Lua: " .. modules_home)
print("[SentinelaBridge] aguardando request.txt; STOP_BRIDGE encerra.")

local last_id = clean(read_file(last_id_path) or "")
local running = true

while running do
    local raw = read_file(request_path)
    if raw and raw ~= "" then
        local req = parse_kv(raw)
        local id = clean(req.id or "")
        if id ~= "" and id ~= last_id then
            append_log("REQUEST id=" .. id .. " command=" .. tostring(req.command or "PING") .. " module=" .. tostring(req.module or ""))
            local ok, result = pcall(execute, req)
            if not ok then
                result = { id=id, status="error", error="bridge_exception", detail=clean(result) }
            end

            local wrote, err = write_file(response_path, encode_kv(result))
            if wrote then
                write_file(last_id_path, id .. "\n")
                last_id = id
                append_log("RESPONSE id=" .. id .. " status=" .. tostring(result.status))
            else
                append_log("WRITE_ERROR id=" .. id .. " error=" .. tostring(err))
            end

            if result.stop == "true" then running = false end
        end
    end

    if running then
        if bmd and bmd.wait then bmd.wait(0.25) else break end
    end
end

append_log("STOP")
print("[SentinelaBridge] encerrado.")
