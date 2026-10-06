# QA - Bilheteria de Cinema

Trabalho de QA do Senac (Prof. Icaro Ferreira) - Grupo 06.

Integrantes: Pedro Valença, Jorge Antônio, Nicolas Tavares, Ygor Sampaio e Davi Felipe.

## Em 30 segundos

Testamos um sistema de bilheteria de cinema feito em Python. A partir de 5 requisitos, escrevemos 12 casos de teste, rodamos tudo de forma automática, registramos os resultados e deixamos o próprio processo decidir se a versão pode ser liberada.

Para provar que funciona, colocamos dois bugs de propósito no sistema e mostramos que os testes pegam os dois.

## Objetivo do trabalho

O foco é o **processo de qualidade**, não o tamanho do sistema. Por isso o sistema testado é pequeno de propósito: cabe num único arquivo (`sistema/cinema.py`) e deixa a atenção no que importa, que é testar, medir e decidir.

O processo segue estes passos:

1. **Requisitos**: definimos 5 regras de negócio que o sistema precisa cumprir.
2. **Casos de teste**: para cada regra, escrevemos de 2 a 3 testes com resultado esperado e severidade.
3. **Execução**: o executor roda cada teste e compara o resultado obtido com o esperado.
4. **Registro**: os resultados vão para CSV e para um relatório HTML.
5. **Decisão**: com base na gravidade das falhas, o processo diz se a versão pode ou não ser liberada.

## Como executar

Precisa do Python 3.8 ou mais novo. Não tem nada para instalar: o projeto usa só a biblioteca padrão do Python.

| Comando | O que faz |
|---|---|
| `python main.py` | Testa o sistema sem bug |
| `python main.py --bug 1` | Testa com o BUG 1 ligado |
| `python main.py --bug 2` | Testa com o BUG 2 ligado |
| `python main.py --comparar` | Roda sem bug e com o BUG 1 e compara |
| `python main.py --comparar --bug 2` | Mesma comparação com o BUG 2 |

Com `--abrir` o relatório abre no navegador no final (exemplo: `python main.py --comparar --abrir`).

No VS Code também dá para rodar com F5. O arquivo `.vscode/launch.json` já tem 4 opções prontas: sem bug, BUG 1, BUG 2 e comparação.

## O sistema testado

O sistema vende ingressos para duas sessões, as duas com preço de R$ 30,00 e assentos de A1 a A5 (dados em `dados/sessoes.json`):

| Sessão | Filme | Classificação |
|---|---|---|
| S1 | Aventura no Espaço | Livre |
| S2 | Noite do Terror | 16 anos |

Quando uma regra é quebrada (assento ocupado, idade abaixo da classificação etc.), o sistema recusa a operação e informa o motivo.

## Requisitos

| Requisito | Regra |
|---|---|
| RF01 Venda | Um assento livre e existente pode ser vendido e fica ocupado. |
| RF02 Assento único | Um assento vendido não pode ser vendido de novo na mesma sessão. |
| RF03 Meia-entrada | Estudantes e pessoas com 60 anos ou mais pagam metade. |
| RF04 Classificação | O cliente precisa ter a idade mínima do filme. |
| RF05 Cancelamento | Um ingresso pode ser cancelado e o assento fica livre. |

## Casos de teste

São 12 casos (CT01 a CT12), com 2 ou 3 por requisito. Eles cobrem três tipos de cenário:

- **Normal** (6 casos): o uso comum, que precisa funcionar.
- **Erro** (4 casos): o que o sistema precisa recusar.
- **Limite** (2 casos): valores exatamente na borda da regra, como 60 anos e 16 anos.

| Teste | Requisito | Tipo | O que testa | Esperado | Severidade |
|---|---|---|---|---|---|
| CT01 | RF01 | Normal | Vender assento livre | Ingresso emitido, A1 ocupado | CRÍTICA |
| CT02 | RF01 | Erro | Vender assento que não existe | Recusado | MÉDIA |
| CT03 | RF02 | Normal | Vender dois assentos diferentes | 2 ingressos | ALTA |
| CT04 | RF02 | Erro | Vender o mesmo assento duas vezes | Recusado | CRÍTICA |
| CT05 | RF03 | Normal | Adulto paga inteira | R$ 30,00 | ALTA |
| CT06 | RF03 | Normal | Estudante paga meia | R$ 15,00 | ALTA |
| CT07 | RF03 | Limite | Cliente com 60 anos paga meia | R$ 15,00 | MÉDIA |
| CT08 | RF04 | Normal | 18 anos compra filme 16 anos | Ingresso emitido | ALTA |
| CT09 | RF04 | Erro | 15 anos compra filme 16 anos | Recusado | CRÍTICA |
| CT10 | RF04 | Limite | 16 anos compra filme 16 anos | Ingresso emitido | MÉDIA |
| CT11 | RF05 | Normal | Cancelar e liberar o assento | A1 livre | ALTA |
| CT12 | RF05 | Erro | Cancelar ingresso que não existe | Recusado | BAIXA |

Total por severidade: 3 críticas, 5 altas, 3 médias e 1 baixa.

### Como o executor funciona

- Cada teste roda com um **cinema novo**, para um não atrapalhar o outro. Se o CT01 vendesse o A1 e o próximo teste usasse o mesmo cinema, ele encontraria o assento ocupado e falharia por causa do teste anterior, não por um defeito.
- O executor compara o resultado **obtido** com o **esperado**. Se forem iguais, o teste passa (PASS). Se não, falha (FAIL).
- Quando o sistema recusa uma operação, o executor registra `Recusado: <motivo>`. Assim os cenários de erro também são comparados com o esperado.

### Como definimos a severidade

Pelo impacto da falha no negócio:

- **CRÍTICA**: vender o mesmo assento para duas pessoas ou vender filme +16 para um menor.
- **ALTA / MÉDIA**: cobrar o preço errado ou falhar num fluxo comum.
- **BAIXA**: cancelar um ingresso que não existe.

## Decisão de QA

No final de cada execução, o processo decide sozinho:

- **LIBERADO**: nenhum teste falhou.
- **LIBERADO COM RESSALVAS**: teve falha, mas nenhuma crítica. O defeito fica para a próxima versão.
- **NÃO LIBERAR**: teve pelo menos uma falha crítica.

## Bugs propositais

Os dois bugs ficam em `sistema/cinema.py`, marcados com `# BUG PROPOSITAL`, e começam desligados. Eles são ligados pela linha de comando com `--bug 1` ou `--bug 2`.

| | BUG 1 | BUG 2 |
|---|---|---|
| O que faz | Pula a checagem de assento ocupado e vende o mesmo assento duas vezes | Usa `>` no lugar de `>=`, então quem tem exatamente 60 anos paga inteira |
| Teste que pega | CT04 (crítico) | CT07 (médio) |
| Resultado | 11 de 12 aprovados (91,7%) | 11 de 12 aprovados (91,7%) |
| Decisão | NÃO LIBERAR | LIBERADO COM RESSALVAS |

## Conclusão

**A taxa de aprovação é a mesma, mas a decisão é diferente.** Contar quantos testes passaram não basta: o que define a liberação é a gravidade do que falhou. Os dois bugs dão 91,7%, mas um quebra uma regra crítica e o outro não.

O BUG 2 também mostra por que testar **valores limite** vale a pena. O erro só aparece com alguém de exatamente 60 anos. Um teste com 65 anos passaria, e o defeito iria para produção sem ninguém perceber.

## O que fica registrado

Cada execução gera ou atualiza três arquivos na pasta `relatorios/`:

| Arquivo | Conteúdo |
|---|---|
| `relatorio_qa.html` | Relatório visual com métricas, defeitos, resumo por requisito e a decisão final |
| `resultados_testes.csv` | O resultado de cada um dos 12 testes da última execução |
| `historico_execucoes.csv` | Uma linha por execução. É a base da comparação entre o antes e o depois |

Os CSV usam `;` como separador e abrem direto no Excel. Para começar do zero, é só apagar os `.html` e `.csv` dessa pasta.

Se algum CSV estiver aberto no Excel durante a execução, ele não é gravado e o terminal mostra um aviso pedindo para fechar o arquivo.

## Estrutura do projeto

```
TrabalhoQA-Grupo06/
├── main.py                  ponto de entrada: lê os comandos e roda o QA
├── config.py                nomes e caminhos usados no projeto
├── sistema/
│   └── cinema.py            o sistema testado (com os 2 bugs propositais)
├── testes/
│   ├── casos_de_teste.py    os 12 casos de teste (CT01 a CT12)
│   └── executor.py          roda cada caso e compara obtido x esperado
├── qa/
│   ├── analise.py           métricas, lista de defeitos e decisão de QA
│   ├── registros.py         gravação dos CSV e comparação antes x depois
│   ├── terminal.py          o que aparece no terminal
│   ├── relatorio_html.py    monta o relatório HTML
│   └── modelo_relatorio.html  modelo visual do relatório
├── dados/
│   ├── requisitos.json      os 5 requisitos
│   └── sessoes.json         as 2 sessões usadas nos testes
└── relatorios/              arquivos gerados a cada execução
```
