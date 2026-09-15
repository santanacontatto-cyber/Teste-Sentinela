# CODEX TASK — instalar e provar a ponte permanente Sentinela ↔ DaVinci

Trabalhe somente nesta branch: `davinci-bridge-v0`.

Objetivo: instalar e testar a arquitetura atual. O bridge é fixo; novas capacidades entram como módulos Lua em `davinci_bridge/modules/`.

## Restrições

- Windows do usuário.
- Custo zero.
- Sem PowerShell.
- Sem privilégios de administrador.
- Não instalar software pago.
- Não abrir portas de rede.
- Não apagar arquivos anteriores do usuário.
- Não alterar documentos existentes no Google Drive.
- Não usar shell através do bridge.
- Não executar código textual arbitrário recebido pela mailbox.
- Pode usar Python já disponível e bibliotecas padrão.

## Faça sozinho

1. Confirme que existem:
   - `davinci_bridge/SentinelaBridge.lua`
   - `davinci_bridge/send_command.py`
   - `davinci_bridge/install_windows.py`
   - `davinci_bridge/modules/project_info.lua`
   - `davinci_bridge/modules/open_page.lua`
   - `davinci_bridge/modules/save_project.lua`
2. Rode:
   - `python -m py_compile davinci_bridge/send_command.py davinci_bridge/install_windows.py davinci_bridge/test_protocol.py`
   - `python -m unittest -v davinci_bridge/test_protocol.py` ou equivalente a partir da pasta correta.
3. Rode `python davinci_bridge/install_windows.py`.
4. Confirme:
   - listener copiado para a pasta `Utility` do Resolve;
   - `%USERPROFILE%\SentinelaBridge\{inbox,outbox,logs,modules}` criado;
   - os três módulos Lua copiados para `modules`.
5. Descubra se o DaVinci Resolve está instalado e informe caminho/versão sem exigir admin.
6. Se puder iniciar o script no Resolve com seu acesso atual, faça. Se houver um único bloqueio de GUI, pare e diga exatamente:
   `PRECISA DE 1 CLIQUE: Workspace > Scripts > SentinelaBridge`
7. Com o listener ativo, execute nesta ordem:
   - `python davinci_bridge/send_command.py ping`
   - `python davinci_bridge/send_command.py run project_info`
   - `python davinci_bridge/send_command.py run open_page --arg page=edit`
8. Não execute `save_project` no primeiro teste.
9. Prova de hot-load, se o listener estiver funcionando:
   - copie/sincronize novamente `project_info.lua` sem reiniciar o listener;
   - rode `run project_info` outra vez;
   - registre que o módulo foi carregado de arquivo separado do bridge.
10. Encerre com `python davinci_bridge/send_command.py stop`.
11. Grave `davinci_bridge/CODEX_RESULT.md` nesta branch com:
   - ambiente encontrado;
   - caminhos instalados;
   - saída literal de cada teste;
   - falhas/erros;
   - confirmação ou não de hot-load;
   - próximo menor passo.

Não peça ao usuário para investigar tecnicamente. Só peça intervenção quando seu acesso ao GUI realmente não conseguir atravessar uma etapa.
