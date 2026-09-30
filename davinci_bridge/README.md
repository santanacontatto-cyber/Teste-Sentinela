# Sentinela ↔ DaVinci Bridge v1

Ponte permanente para Windows entre Sentinela/Codex e Lua rodando **dentro** do DaVinci Resolve.

## Arquitetura

```text
Sentinela / Codex
      ↓
request.txt / response.txt
      ↓
SentinelaBridge.lua  ← ponte fixa
      ↓
modules/*.lua        ← capacidades que podem mudar sem reconstruir a ponte
      ↓
DaVinci Resolve API
```

A regra central do v1 é simples: **a ponte não cresce junto com cada automação**. Ela só recebe uma requisição, carrega um módulo Lua local por nome e devolve o resultado. Novas capacidades entram como novos módulos Lua.

Isso permite que montagem, Fusion, áudio, render, inspeção de projeto e verificações sejam desenvolvidos depois sem trocar o transporte.

## Restrições mantidas

- custo zero;
- sem PowerShell;
- sem admin;
- sem portas de rede;
- sem pacotes Python de terceiros;
- sem shell pelo bridge;
- sem `eval` de código textual;
- sem caminho arbitrário de módulo;
- módulos aceitos apenas por nome simples (`A-Z`, `a-z`, `0-9`, `_`, `-`).

## Hot-load de módulos

O bridge usa `loadfile()` em **cada** requisição `RUN`. Portanto, quando um arquivo em `%USERPROFILE%\SentinelaBridge\modules\` é atualizado, a próxima chamada já usa a nova versão. Não é necessário reconstruir nem reiniciar a ponte para cada função nova.

O módulo deve retornar uma função Lua:

```lua
return function(ctx, req)
    -- ctx.resolve = API do Resolve
    -- ctx.snapshot(resolve) = snapshot básico
    -- req["arg.nome"] = argumentos enviados
    return { status="ok", resultado="..." }
end
```

Também é aceito `return { run = function(ctx, req) ... end }`.

## Arquivos

- `SentinelaBridge.lua` — listener/dispatcher fixo dentro do Resolve.
- `send_command.py` — cliente local genérico.
- `install_windows.py` — instala o listener e sincroniza módulos, sem admin.
- `modules/` — capacidades Lua substituíveis.
- `CODEX_TASK.md` — roteiro para o Codex instalar e provar tudo no PC real.

## Instalação

No checkout da branch:

```text
python davinci_bridge/install_windows.py
```

O listener vai para:

```text
%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility\SentinelaBridge.lua
```

A mailbox e os módulos ficam em:

```text
%USERPROFILE%\SentinelaBridge\
  inbox\
  outbox\
  logs\
  modules\
```

## Primeiro teste real

1. Reiniciar o Resolve se necessário.
2. Executar uma vez `Workspace > Scripts > SentinelaBridge`.
3. Testar a ponte:

```text
python davinci_bridge/send_command.py ping
```

4. Testar módulo Lua:

```text
python davinci_bridge/send_command.py run project_info
```

5. Testar parâmetro para módulo:

```text
python davinci_bridge/send_command.py run open_page --arg page=edit
```

6. Encerrar listener:

```text
python davinci_bridge/send_command.py stop
```

## Módulos iniciais

- `project_info.lua` — leitura do projeto/timeline atual.
- `open_page.lua` — muda entre páginas válidas do Resolve.
- `save_project.lua` — salva o projeto apenas quando chamado explicitamente.

Esses módulos existem só para provar que o transporte é genérico. Eles **não definem o limite da ponte**.

## Critério de sucesso

A ponte está provada quando:

1. Codex instala sem admin;
2. Resolve inicia `SentinelaBridge`;
3. `ping` retorna dados do Resolve real;
4. `run project_info` executa um arquivo Lua separado do listener;
5. uma alteração de módulo pode ser sincronizada e usada sem reconstruir o listener;
6. tudo fica registrado no log local.

Depois disso, a ponte deixa de ser parte do problema: as novas capacidades passam a ser trabalho de módulos Lua.
