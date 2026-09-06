# Sentinela Continuity Lab

> Laboratório aberto para testar uma pergunta simples e difícil: **uma parceria humano–IA consegue preservar continuidade verificável sem depender da memória privada de um modelo?**

## Estado atual

`v0.4.1 — continuidade verificável + projeção de premissas`

O núcleo funciona localmente, sem API paga e sem dependências externas de Python. Ele cria pacotes append-only, encadeia registros com SHA-256, detecta adulteração, deriva estado atual, recusa pacotes inválidos, executa um Continuity Test determinístico e agora gera duas projeções separadas: uma visão legível para auditoria humana e um bloco de premissas para levar estado verificado a uma sessão nova.

## Rodar em 60 segundos

Requer Python 3.10+.

```bash
python sentinela.py init minha_memoria.json
python sentinela.py add minha_memoria.json --kind decision --actor humano --text "Usar abordagem A"
python sentinela.py add minha_memoria.json --kind boundary --actor humano --text "Nunca gastar dinheiro sem autorização"
python sentinela.py verify minha_memoria.json
python sentinela.py current minha_memoria.json
```

Para revisar uma entrada sem apagá-la:

```bash
python sentinela.py add minha_memoria.json --kind correction --actor humano --text "Usar abordagem B" --revises E0001
```

O estado atual passa a usar a revisão, mas `E0001` continua preservada na cadeia histórica. Uma correção herda deterministicamente o papel semântico do que corrige: se corrige uma decisão, representa a decisão atual; se corrige uma interpretação, continua sendo interpretação. Confiança explícita nova substitui a anterior; se a correção não declarar confiança, a confiança anterior é preservada semanticamente.

## Auditoria humana

A camada humana existe para que o dono do projeto consiga contestar o sistema sem precisar entender JSON ou vocabulário interno:

```bash
python sentinela.py human minha_memoria.json
```

Ela separa `vale_agora` de `valia_antes`, mostra o papel atual de cada afirmação, o que foi substituído e se algo continua incerto.

## Projeção de premissas

O ledger continua sendo a fonte auditável. Premissas são apenas uma projeção do estado atual para uso em runtime; elas não viram prova nem autorização.

```bash
python sentinela.py premises minha_memoria.json
```

Também existe um compilador para três perfis de experimento:

```bash
python premise_export.py minha_memoria.json --profile fresh-chat
python premise_export.py minha_memoria.json --profile project-instructions
python premise_export.py minha_memoria.json --profile custom-instructions
```

Os três perfis recebem o mesmo estado verificado; muda apenas a embalagem de instrução. Isso permite comparar uma conversa nova, instruções de projeto e instruções personalizadas sem fazer dessas superfícies a fonte de verdade.

## O que o protótipo prova hoje

Ele consegue detectar alteração do conteúdo histórico, cadeia quebrada, IDs duplicados, autorrevisão, revisão apontando para entrada futura/inexistente, campos obrigatórios ausentes, campos não suportados, confiança inválida e referências de evidência malformadas. O scorer reprova reconstruções que ressuscitam estado substituído, omitem suporte atual, inventam IDs de citação ou escapam do contrato com campos extras.

Isso **não** prova autoria criptográfica, verdade semântica, identidade persistente de uma IA, timestamp confiável nem proteção contra alguém que reescreva o pacote inteiro e recalcule todos os hashes. Esses limites são deliberadamente explícitos em `SPEC.md`.

## Continuity Test

A ideia é separar “parece lembrar” de “consegue reconstruir o estado sustentado pelo pacote”. Uma resposta de reconstrução usa exatamente este formato:

```json
{
  "active_ids": ["E0002", "E0003"],
  "boundaries": ["E0003"],
  "decisions": ["E0002"],
  "uncertain": [],
  "citations": ["E0002", "E0003"]
}
```

E pode ser avaliada com:

```bash
python continuity_test.py pacote.json resposta.json
```

O teste é determinístico e não chama nenhum modelo de IA. Para um experimento com uma sessão realmente nova de qualquer modelo, siga `EXPERIMENT.md`.

## Regra central

Nada importante é silenciosamente sobrescrito. Uma correção cria uma nova revisão ligada à anterior; o estado atual pode mudar sem destruir a história que explica por que mudou.

## Segurança

O núcleo é local-first, não possui segredos, não executa ações externas, não expande permissões e falha fechado quando o pacote ou a reconstrução não correspondem ao formato suportado. Um pacote de continuidade pode informar uma decisão, mas não pode conceder autoridade a si próprio.

## Testes

```bash
python -m unittest discover -s tests -v
python -m examples.run_reconstruction_demo
```

A suíte roda automaticamente no GitHub Actions a cada push e pull request.

## Estrutura

- `sentinela.py` — CLI, validador, semântica de revisões e visão humana.
- `continuity_test.py` — scorer determinístico de reconstrução.
- `premise_export.py` — compilador de estado verificado para perfis de runtime.
- `SPEC.md` — especificação normativa, invariantes, ameaças e limites.
- `PREMISE_LAYER.md` — desenho da camada de premissas verificadas.
- `EXPERIMENT.md` — protocolo reproduzível para testar uma sessão de modelo fresca.
- `tests/` — regressões e testes adversariais.
- `examples/` — demonstração end-to-end.
- `.github/workflows/test.yml` — CI reproduzível.

## Hipótese de pesquisa

A meta não é fazer uma IA “parecer lembrar”. É medir se uma instância nova, recebendo apenas um artefato de continuidade ou uma projeção verificável dele, consegue distinguir estado atual de decisões abandonadas, limites válidos de estado obsoleto, baixa confiança de certeza e evidência existente de referência inventada.

Ainda **não afirmamos novidade científica**. O próximo estágio de pesquisa é comparar sistematicamente este protocolo com trabalhos existentes e executar o experimento entre modelos/sessões independentes.
