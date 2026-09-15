-- Modulo Lua: open_page
-- Uso: RUN module=open_page arg.page=edit

local allowed = {
    media=true, cut=true, edit=true, fusion=true,
    color=true, fairlight=true, deliver=true,
}

return function(ctx, req)
    local page = string.lower(req["arg.page"] or "")
    if not allowed[page] then
        return { status="error", error="invalid_page", requested_page=page }
    end

    local ok = ctx.resolve:OpenPage(page)
    local result = ctx.snapshot(ctx.resolve)
    result.open_page = page
    result.open_page_ok = tostring(ok == true)
    return result
end
