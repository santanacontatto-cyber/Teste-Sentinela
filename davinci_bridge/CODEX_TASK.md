# CODEX TASK — instalar e provar a ponte Sentinela ↔ DaVinci

Trabalhe somente nesta branch: `davinci-bridge-v0`.

Objetivo: instalar e testar a ponte já desenhada. Não substitua a arquitetura antes do primeiro teste real.

## Restrições

- Windows do usuário.
- Sem PowerShell.
- Sem privilégios de administrador.
- Não instalar software pago.
- Não abrir portas de rede.
- Não apagar arquivos anteriores do usuário.
- Não alterar documentos existentes no Google Drive.
- Não executar código recebido arbitrariamente pelo bridge.
- Pode usar Python já disponível no seu ambiente e bibliotecas padrão.

## Faça sozinho

1. Inspecione o workspace e procure rastros da ponte antiga (Lua, DaVinci, Resolve, Fusion, bridge, sentinel/sentinela). Apenas relate se encontrar; não restaure por cima do v0.
2. Confirme que `davinci_bridge/SentinelaBridge.lua`, `send_command.py` e `install_windows.py` estão presentes.
3. Rode testes estáticos possíveis no Python (`py_compile`).
4. Rode `python davinci_bridge/install_windows.py`.
5. Confirme que o Lua foi copiado para a pasta Utility do usuário e que `%USERPROFILE%\SentinelaBridge\{inbox,outbox,logs}` existe.
6. Descubra se DaVinci Resolve está instalado e informe versão/caminho se isso puder ser feito sem admin.
7. Se for possível iniciar/testar o script no Resolve com as ferramentas autorizadas do seu ambiente, faça. Caso o único bloqueio seja um clique no menu do Resolve, pare nesse ponto e diga exatamente: `PRECISA DE 1 CLIQUE: Workspace > Scripts > SentinelaBridge`.
8. Assim que o listener estiver ativo, rode:
   - `python davinci_bridge/send_command.py ping`
   - `python davinci_bridge/send_command.py project_info`
   - `python davinci_bridge/send_command.py open_page --page edit`
9. Não rode `save_project` automaticamente no primeiro teste.
10. Encerre com `python davinci_bridge/send_command.py stop_bridge`.
11. Grave um relatório novo em `davinci_bridge/CODEX_RESULT.md` nesta branch com:
   - ambiente encontrado;
   - rastros da ponte antiga;
   - arquivos instalados;
   - saída literal dos testes;
   - falhas/erros;
   - próximo menor passo.

Não peça ao usuário para fazer investigação técnica. Só peça intervenção quando for impossível atravessar uma etapa do GUI com seu acesso atual.
