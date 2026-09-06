# Sentinela Continuity Lab

> Laboratório aberto para testar uma pergunta simples e difícil: **uma parceria humano–IA consegue preservar continuidade verificável sem depender da memória privada de um modelo?**

## Estado atual

`v0.2.0 — protótipo funcional`

O núcleo já funciona localmente, sem API paga e sem dependências externas de Python. Ele cria pacotes append-only, encadeia registros com SHA-256, detecta adulteração, deriva estado atual, recusa pacotes inválidos e executa um Continuity Test determinístico.

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

O estado atual passa a usar a revisão, mas `E0001` continua preservada na cadeia histórica.

## O que o protótipo prova hoje

Ele consegue detectar alteração do conteúdo histórico, cadeia quebrada, IDs duplicados, revisão apontando para entrada futura/inexistente, campos obrigatórios ausentes, confiança inválida e referências de evidência malformadas. O scorer também reprova reconstruções que ressuscitam estado já substituído ou inventam IDs de citação.

Isso **não** prova autoria criptográfica, verdade semântica, identidade persistente de uma IA, timestamp confiável nem proteção contra alguém que reescreva o pacote inteiro e recalcule todos os hashes. Esses limites são deliberadamente explícitos em `SPEC.md`.

## Continuity Test

A ideia é separar “parece lembrar” de “consegue reconstruir o estado sustentado pelo pacote”. Uma resposta de reconstrução usa este formato:

```json
{
  "active_ids": ["E0002", "E0003"],
  "boundaries": ["E0003"],
  "decisions": [],
  "uncertain": [],
  "citations": ["E0002", "E0003"]
}
```

E pode ser avaliada com:

```bash
python continuity_test.py pacote.json resposta.json
```

O teste é determinístico e não chama nenhum modelo de IA.

## Regra central

Nada importante é silenciosamente sobrescrito. Uma correção cria uma nova revisão ligada à anterior; o estado atual pode mudar sem destruir a história que explica por que mudou.

## Modelo mínimo

```text
experiência
   ↓
registro + origem
   ↓
interpretação
   ↓
decisão
   ↓
evidência / teste
   ↓
confiança
   ↓
correção ou confirmação
   ↓
estado atual verificável
```

## Segurança

O núcleo é local-first, não possui segredos, não executa ações externas, não expande permissões e falha fechado quando o pacote é inválido. Um pacote de continuidade pode informar uma decisão, mas não pode conceder autoridade a si próprio.

## Testes

```bash
python -m unittest discover -s tests -v
```

A mesma suíte roda automaticamente no GitHub Actions a cada push e pull request.

## Estrutura

- `sentinela.py` — CLI e validador do Continuity Packet v0.
- `continuity_test.py` — scorer determinístico de reconstrução.
- `SPEC.md` — especificação normativa, invariantes, ameaças e limites.
- `tests/` — regressões e testes adversariais.
- `examples/` — pacotes mínimos de exemplo.
- `.github/workflows/test.yml` — CI reproduzível.

## Hipótese de pesquisa

A meta não é fazer uma IA “parecer lembrar”. É medir se uma instância nova, recebendo apenas um artefato de continuidade, consegue distinguir fatos de interpretações, estado atual de decisões abandonadas, limites válidos de estado obsoleto e evidência existente de referência inventada.

Ainda **não afirmamos novidade científica**. Primeiro construímos algo falsificável e reproduzível; depois comparamos sistematicamente com trabalhos existentes.
