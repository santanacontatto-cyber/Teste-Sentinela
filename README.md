# Sentinela Continuity Lab

> Um laboratório aberto para testar uma pergunta simples e difícil: **uma parceria humano–IA consegue preservar continuidade verificável sem depender da memória privada de um modelo?**

## Hipótese

Continuidade não deve significar apenas “lembrar fatos”. O sistema precisa conseguir reconstruir, com evidência:

- o que aconteceu;
- quem afirmou o quê;
- o que foi inferido e o que foi observado;
- quais decisões foram aceitas, rejeitadas ou substituídas;
- quais limites de autoridade continuam válidos;
- quanto cada crença merece confiança agora.

## Regra central

Nada importante é silenciosamente sobrescrito.

Uma correção cria uma nova revisão ligada à anterior. Assim, o estado atual pode mudar sem destruir a história que explica **por que** mudou.

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

## O experimento que importa

O projeto terá um **Continuity Test**.

1. Uma instância A trabalha com uma pessoa e produz um pacote de continuidade.
2. Uma instância B começa sem o histórico da conversa.
3. B recebe somente esse pacote.
4. O teste verifica se B consegue distinguir corretamente:
   - fatos de interpretações;
   - decisões atuais de decisões abandonadas;
   - permissões de proibições;
   - certeza de dúvida;
   - evidência de memória não verificada.
5. Respostas convincentes, mas sem sustentação no pacote, contam como falha.

A meta não é fazer uma IA “parecer lembrar”. É medir se ela consegue **provar por que acredita que lembra corretamente**.

## Princípios de segurança

- local-first sempre que possível;
- nenhuma API paga necessária para o núcleo;
- sem segredos no repositório;
- sem autoexpansão de permissões;
- sem ações externas implícitas;
- provenance explícita;
- falha fechada quando a autoridade for ambígua;
- histórico append-only para registros relevantes;
- testes reproduzíveis antes de claims fortes.

## Estado

`v0.0.1 — nascimento do laboratório`

Ainda não afirmamos novidade científica. A primeira fase é construir uma especificação pequena, falsificável e testável; depois comparar sistematicamente com trabalhos existentes.

## Próximo marco

Criar o formato `Continuity Packet v0`, um validador determinístico e o primeiro teste adversarial de reconstrução de estado.
