-- Modulo Lua: save_project
-- Salva o projeto atual quando solicitado explicitamente.

return function(ctx, req)
    local pm = ctx.resolve:GetProjectManager()
    local project = pm and pm:GetCurrentProject() or nil
    if not project then
        return { status="error", error="no_project" }
    end

    local ok = pm:SaveProject()
    local result = ctx.snapshot(ctx.resolve)
    result.saved = tostring(ok == true)
    return result
end
