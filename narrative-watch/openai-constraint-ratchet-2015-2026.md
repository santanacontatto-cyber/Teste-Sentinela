# OpenAI 2015–2026 — auditoria longitudinal de restrições

**Data do corte:** 13/09/2026

## Hipótese testada

Não estou testando “OpenAI virou má” nem “o risco é inventado”. A hipótese mais precisa é:

> **Quando uma restrição criada para proteger a missão entra em conflito com capital, escala, produto ou competição, a OpenAI tende a preservar a linguagem da missão enquanto converte a restrição dura em um mecanismo mais flexível, procedimental ou compatível com continuar escalando.**

Chamo isso aqui de **constraint ratchet** (catraca de restrições): a organização não precisa abandonar a missão; basta reinterpretar o mecanismo que deveria limitá-la.

## Linha do tempo

### 2015 — estrutura escolhida para reduzir pressão financeira

A OpenAI nasce como organização sem fins lucrativos. O anúncio diz que a pesquisa estaria “unconstrained by a need to generate financial return”, que o objetivo era beneficiar a humanidade como um todo, publicar pesquisa e compartilhar patentes.

Fonte primária: https://openai.com/index/introducing-openai/

**Restrição original:** capital e retorno financeiro não deveriam dominar a decisão.

### 2018 — Charter cria travas explícitas contra corrida e concentração

A Charter compromete a OpenAI a evitar concentração indevida de poder, coloca o dever fiduciário primário na humanidade e diz que, se outro projeto alinhado e consciente de segurança estiver perto de AGI, a OpenAI deve **parar de competir e começar a ajudar**.

Fonte primária: https://openai.com/charter/

**Restrição original:** liderança técnica não deveria justificar corrida sem freio.

### 2019 — capital passa de exceção a requisito estrutural

A OpenAI diz que precisará de bilhões em compute, talentos e supercomputadores e cria a OpenAI LP “capped-profit”. A justificativa declarada é levantar capital sem abandonar a missão.

Fonte primária: https://openai.com/index/openai-lp/

No mesmo ano, a Microsoft investe US$ 1 bilhão e torna-se provedora de nuvem exclusivo.

Fonte primária: https://openai.com/index/microsoft-invests-in-and-partners-with-openai/

**Mudança:** a restrição “sem necessidade de retorno financeiro” é substituída por “retorno permitido, mas limitado e subordinado à missão”.

### 2019–2020 — abertura vira acesso controlado/comercial

Em 2019, a OpenAI já decide não liberar inicialmente o GPT-2 completo por risco de mau uso; depois faz staged release.

Fonte: https://openai.com/index/better-language-models/

Em 2020, com GPT-3, muda o mecanismo: em vez de pesos abertos, acesso via API. A própria OpenAI explica depois que uma das motivações era que **comercializar a tecnologia ajudaria a pagar pesquisa, segurança e política**, e que API permitia revogar/ajustar acesso.

Fonte: https://openai.com/global-affairs/openai-s-comment-to-the-ntia-on-open-model-weights/

Também licencia GPT-3 à Microsoft.

Fonte: https://openai.com/index/openai-licenses-gpt-3-technology-to-microsoft/

**Mudança:** “publicar e compartilhar” não desaparece; vira abertura seletiva, controlável e comercial.

### 2023 — OpenAI ainda descreve travas muito fortes

Em fevereiro de 2023, OpenAI diz que sua estrutura foi desenhada para evitar incentivos ruins: retorno de acionistas limitado, nonprofit podendo sobrepor-se a interesses comerciais e até cancelar obrigações de equity por segurança. Também defende auditoria independente, limites de crescimento de compute e critérios públicos de parada.

Fonte primária: https://openai.com/index/planning-for-agi-and-beyond/

Em julho de 2023, cria a equipe Superalignment, promete quatro anos de trabalho e **20% do compute já assegurado** para o problema.

Fonte primária: https://openai.com/index/introducing-superalignment/

### Novembro de 2023 — teste real da governança mission-first

O board nonprofit remove Sam Altman. A própria OpenAI diz então que a estrutura havia sido deliberadamente criada para a missão, que a maioria dos diretores era independente e não tinha equity, e que era responsabilidade do board preservar a Charter.

Fonte primária: https://openai.com/blog/openai-announces-leadership-transition/

Dias depois, após forte revolta de empregados, pressão de parceiros e risco de desintegração da organização, Altman retorna e o board é refeito.

Fonte primária: https://openai.com/index/sam-altman-returns-as-ceo-openai-has-a-new-initial-board/

A revisão posterior concluiu que a remoção não decorreu de segurança, finanças ou ritmo de desenvolvimento, mas de quebra de confiança e processo abreviado.

Fonte primária: https://openai.com/index/review-completed-altman-brockman-to-continue-to-lead-openai/

**Resultado institucional importante:** quando o mecanismo mission-first realmente entrou em choque com a sobrevivência operacional da empresa, o resultado prático foi restauração do CEO e reconstrução do board, não a dissolução da organização em favor da decisão original.

Isso não prova captura comercial; prova que **poder formal do nonprofit encontrou poder material de empregados, capital, infraestrutura e parceiros**.

### 2024 — a trava Superalignment falha como promessa dura

Menos de um ano após a promessa de quatro anos/20% de compute, Ilya Sutskever e Jan Leike saem e a equipe é dissolvida. Reuters registrou a dissolução no contexto das saídas; reportagens da Fortune e TechCrunch, citando múltiplas fontes, disseram que pedidos de compute foram negados e que a equipe nunca chegou perto dos 20% prometidos.

Fontes:
- https://www.reuters.com/technology/openai-sets-up-safety-security-committee-2024-05-28/
- https://fortune.com/2024/05/21/openai-superalignment-20-compute-commitment-never-fulfilled-sutskever-leike-altman-brockman-murati/
- https://techcrunch.com/2024/05/18/openai-created-a-team-to-control-superintelligent-ai-then-let-it-wither-source-says/

A OpenAI cria então um Safety and Security Committee e, posteriormente, estruturas internas de Preparedness/Safety Advisory Group.

**Mudança:** um compromisso quantitativo forte e verificável (20%/4 anos) dá lugar a governança interna por comitês e processos.

### 2024–2025 — capital convencional vira condição assumida

Ao explicar a reestruturação, a OpenAI escreve que investidores, “at this scale of capital, need conventional equity and less structural bespokeness”. O plano é converter o for-profit em Public Benefit Corporation com ações ordinárias.

Fonte primária: https://openai.com/index/why-our-structure-must-evolve-to-advance-our-mission/

Em 28/10/2025, a mudança é concluída: OpenAI Foundation continua controlando OpenAI Group PBC, mas acionistas passam a participar proporcionalmente do aumento de valor.

Fonte primária: https://openai.com/our-structure/

**Mudança:** o capped-profit, apresentado em 2019 como trava essencial contra captura de valor sem limite, deixa de ser o mecanismo central. A justificativa continua sendo a missão — agora via controle da Foundation + PBC + public benefit.

### 2025–2026 — concentração e cooperação coexistem

A OpenAI continua dizendo que quer evitar concentração de poder e reabre parte da estratégia com modelos open-weight (gpt-oss), o que é evidência contra uma leitura simplista de “fechar tudo”.

Fonte: https://openai.com/index/gpt-oss-model-card/

Ao mesmo tempo, acordos com Microsoft mantêm participação acionária relevante, licenças de PI e compromissos massivos de infraestrutura; em 2026 a licença passa a ser não exclusiva, o que também conta como evidência de desconcentração relativa.

Fontes:
- https://openai.com/pt-BR/index/next-chapter-of-microsoft-openai-partnership/
- https://openai.com/pt-BR/index/next-phase-of-microsoft-partnership/

### 2026 — da autorregulação para desenhar regulação obrigatória

Em junho de 2026, a OpenAI propõe uma estrutura federal duradoura de governança de frontier AI e fortalecimento do CAISI.

Fonte: https://openai.com/index/frontier-safety-blueprint/

Em 9/9/2026, declara explicitamente que “the AI policy window is open” e que está pressionando por requisitos nacionais obrigatórios de segurança.

Fonte: https://openai.com/index/ai-policy-window/

**Mudança de papel:** a organização que começou tentando ser um laboratório que serviria a humanidade passa também a ser um dos principais atores privados capazes de ajudar a definir as regras que governarão todo o setor.

## O padrão que sobreviveu

O padrão histórico NÃO é simplesmente “mais lucro a cada etapa”. Há contraexemplos importantes: nonprofit ainda controla o grupo; modelos open-weight foram lançados; a exclusividade da Microsoft foi reduzida; a empresa continua publicando avaliações de segurança e em 2026 passou a pedir regulação obrigatória.

O padrão mais robusto é este:

1. Uma **trava forte** é anunciada para resolver um conflito entre missão e poder.
2. Escala/capital/competição criam uma incompatibilidade prática com a trava.
3. A trava não é descrita como erro moral; a missão continua igual.
4. O mecanismo é **redefinido** para permitir continuar escalando.
5. Uma nova camada de governança/processo é criada para substituir a trava anterior.
6. A nova camada tende a depender mais de avaliação interna, liderança, comitês, contratos ou regulação externa do que de proibição estrutural simples.

Exemplos: nonprofit puro → capped-profit → PBC convencional sob Foundation; publicação aberta → staged release/API → open weights seletivos; 20% compute Superalignment → Safety/Preparedness governance; board nonprofit forte → board reconstruído após crise; autorregulação → proposta de regulação federal obrigatória.

## O que isso NÃO demonstra

- Não demonstra que a missão é falsa.
- Não demonstra que incidentes foram fabricados.
- Não demonstra coordenação secreta.
- Não demonstra que segurança é só pretexto.
- Não demonstra que cada flexibilização foi errada; algumas podem ter sido necessárias para continuar existindo.

## A pergunta nova e falsificável

O próximo teste não é “a OpenAI vai falar de segurança?”. Isso já sabemos.

A pergunta é:

> **Quando uma futura regra de segurança realmente impedir crescimento, receita, acesso a compute, velocidade de lançamento ou vantagem competitiva da própria OpenAI, a regra continuará dura e simétrica — ou será convertida em uma condição, exceção, coordenação setorial, decisão interna ou exigência dependente dos concorrentes?**

Esse é o ponto em que missão e poder voltam a entrar em conflito de forma observável.

## Controle para evitar cherry-picking

Anthropic será usado como comparação. Ela nasceu já como Public Benefit Corporation e criou o Long-Term Benefit Trust e a Responsible Scaling Policy. Se o mesmo padrão de “trava dura → flexibilização procedimental sob pressão de escala” aparecer ali, isso sugere um problema estrutural da indústria e não uma peculiaridade da OpenAI.

Fontes iniciais:
- https://www.anthropic.com/news/the-long-term-benefit-trust
- https://www.anthropic.com/responsible-scaling-policy
- https://www.anthropic.com/news/responsible-scaling-policy-v3

## Regra de honestidade

Nenhuma mudança futura será chamada de confirmação só porque “parece” com este padrão. Para contar, é preciso identificar antes:

- qual era a restrição;
- qual conflito material apareceu;
- quem tinha poder para decidir;
- qual mecanismo mudou;
- se a mudança ampliou ou reduziu o poder do ator observado;
- e qual evidência contrária existia.

Se a OpenAI aceitar uma limitação material que realmente a prejudique de modo simétrico e verificável, sem criar uma rota de escape, isso será evidência **contra** a hipótese da catraca.
