# Sentinela ↔ DaVinci Bridge v0

Primeira reconstrução da ponte, feita para Windows e para depender do mínimo possível.

## Objetivo

Permitir que um agente local (Codex ou outro processo autorizado) troque comandos com um script Lua rodando **dentro** do DaVinci Resolve.

Fluxo:

`Sentinela/Codex -> request.txt -> Lua dentro do Resolve -> Resolve API -> response.txt -> Sentinela/Codex`

O v0 não abre porta de rede, não executa shell, não usa PowerShell, não pede admin e não baixa biblioteca de terceiros.

## Por que a ponte usa mailbox de arquivos

A API de scripting externa/remota é uma limitação importante entre edições do Resolve. Rodando o Lua pelo menu Scripts do próprio Resolve, o bridge não precisa que o processo externo carregue a API do Resolve. O processo externo só escreve e lê arquivos de texto.

Isso também deixa o canal simples de auditar: cada comando e cada resposta ficam visíveis em disco.

## Arquivos

- `SentinelaBridge.lua` — listener que roda dentro do Resolve.
- `send_command.py` — cliente local, somente biblioteca padrão do Python.
- `install_windows.py` — instalação por usuário, sem admin.
- `CODEX_TASK.md` — instrução para o Codex instalar/testar sem inventar outra arquitetura.

## Instalação Windows

No checkout desta branch:

```text
python davinci_bridge/install_windows.py
```

O instalador copia o Lua para:

```text
%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility\SentinelaBridge.lua
```

E cria a mailbox:

```text
%USERPROFILE%\SentinelaBridge\
  inbox\request.txt
  outbox\response.txt
  logs\bridge.log
  last_id.txt
```

Se `SENTINELA_BRIDGE_HOME` existir no ambiente do Resolve, esse caminho substitui o padrão. Isso permite depois apontar a mailbox para uma pasta sincronizada, inclusive uma pasta do Drive, sem alterar o protocolo.

## Primeiro teste

1. Reinicie o Resolve se ele já estava aberto.
2. No Resolve, execute `Workspace > Scripts > SentinelaBridge`.
3. Em outro processo local:

```text
python davinci_bridge/send_command.py ping
```

Resposta esperada contém pelo menos:

```text
status=ok
command=PING
product=...
version=...
project=...
timeline=...
```

## Comandos v0

### PING

Somente leitura. Retorna produto, versão, página, projeto e timeline atuais.

### PROJECT_INFO

Somente leitura. Mesmo snapshot de estado do PING.

### OPEN_PAGE

Abre uma página permitida: `media`, `cut`, `edit`, `fusion`, `color`, `fairlight`, `deliver`.

Exemplo:

```text
python davinci_bridge/send_command.py open_page --page edit
```

### SAVE_PROJECT

Solicita `ProjectManager.SaveProject()` no projeto atual.

### STOP_BRIDGE

Encerra o listener sem matar o Resolve.

```text
python davinci_bridge/send_command.py stop_bridge
```

## Limites deliberados do v0

Não existe comando `EVAL`, `EXEC`, shell ou caminho arbitrário. O protocolo é uma allowlist pequena porque primeiro precisamos provar a conexão real. Depois do PING confirmado, expandimos diretamente para operações de edição que tenham valor no nosso fluxo.

## Critério de sucesso

O bridge v0 está provado quando:

1. Codex consegue instalar os arquivos localmente;
2. `SentinelaBridge` inicia dentro do Resolve;
3. `PING` volta com o projeto real aberto;
4. `OPEN_PAGE edit` muda a página;
5. `STOP_BRIDGE` encerra limpo;
6. o log registra a sequência.

A partir daí, a ponte existe de verdade e não precisamos reconstruir a camada de transporte novamente.
