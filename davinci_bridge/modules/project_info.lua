-- Modulo Lua: project_info
-- Retorna um snapshot do Resolve/projeto/timeline usando o contexto fornecido pela ponte.

return function(ctx, req)
    return ctx.snapshot(ctx.resolve)
end
