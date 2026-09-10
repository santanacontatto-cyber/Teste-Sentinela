-- SentinelaBridge v0
-- File-mailbox bridge for DaVinci Resolve + Lua.
-- Designed to run from Resolve's Scripts menu. No network socket, no shell execution.
-- External tools (e.g. Codex) only write request.txt and read response.txt.

local bridge = {}

local SEP = package.config:sub(1, 1)
local home = os.getenv("SENTINELA_BRIDGE_HOME")
if not home or home == "" then
    local user = os.getenv("USERPROFILE") or os.getenv("HOME") or "."
    home = user .. SEP .. "SentinelaBridge"
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

local function append_log(line)
    local f = io.open(log_path, "a")
    if f then
        f:write(os.date("!%Y-%m-%dT%H:%M:%SZ") .. " " .. tostring(line) .. "\n")
        f:close()
    end
end

local function parse_kv(text)
    local t = {}
    for line in tostring(text):gmatch("[^\r\n]+") do
        local k, v = line:match("^([%w_%-]+)%s*=%s*(.*)$")
        if k then t[k] = v end
    end
    return t
end

local function clean(v)
    v = tostring(v or "")
    v = v:gsub("[\r\n]", " ")
    return v
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

local allowed_pages = {
    media=true, cut=true, edit=true, fusion=true,
    color=true, fairlight=true, deliver=true
}

local function execute(req)
    local r = get_resolve()
    if not r then
        return { id=req.id or "", status="error", error="resolve_unavailable" }
    end

    local cmd = string.upper(req.command or "PING")
    local result

    if cmd == "PING" or cmd == "PROJECT_INFO" then
        result = snapshot(r)

    elseif cmd == "OPEN_PAGE" then
        local page = string.lower(req.page or "")
        if not allowed_pages[page] then
            result = { status="error", error="invalid_page" }
        else
            local ok = r:OpenPage(page)
            result = snapshot(r)
            result.open_page = page
            result.open_page_ok = tostring(ok == true)
        end

    elseif cmd == "SAVE_PROJECT" then
        local pm = r:GetProjectManager()
        local project = pm and pm:GetCurrentProject() or nil
        if not project then
            result = { status="error", error="no_project" }
        else
            local ok = pm:SaveProject()
            result = snapshot(r)
            result.saved = tostring(ok == true)
        end

    elseif cmd == "STOP_BRIDGE" then
        result = snapshot(r)
        result.stop = "true"

    else
        result = { status="error", error="unsupported_command", command=cmd }
    end

    result.id = req.id or ""
    result.command = cmd
    return result
end

append_log("START home=" .. home)
print("[SentinelaBridge] ativo em: " .. home)
print("[SentinelaBridge] aguardando request.txt; STOP_BRIDGE encerra.")

local last_id = clean(read_file(last_id_path) or "")
local running = true

while running do
    local raw = read_file(request_path)
    if raw and raw ~= "" then
        local req = parse_kv(raw)
        local id = clean(req.id or "")
        if id ~= "" and id ~= last_id then
            append_log("REQUEST id=" .. id .. " command=" .. tostring(req.command or "PING"))
            local ok, result = pcall(execute, req)
            if not ok then
                result = { id=id, status="error", error="lua_exception", detail=clean(result) }
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
