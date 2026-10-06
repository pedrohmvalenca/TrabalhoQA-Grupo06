# QA - Bilheteria de Cinema

Trabalho de QA do Senac (Prof. Icaro Ferreira).

Integrantes: Pedro Valença, Jorge Antônio, Nicolas Tavares, Ygor Sampaio e Davi Felipe.

Testamos um sistema simples de bilheteria de cinema em Python: escrevemos os casos de teste a partir dos requisitos, rodamos, registramos os resultados e tomamos a decisão de liberar ou não a versão.

## Como executar

Precisa do Python 3.8 ou mais novo. Não tem nada para instalar.

| Comando | O que faz |
|---|---|
| `python main.py` | Testa o sistema sem bug |
| `python main.py --bug 1` | Testa com o BUG 1 ligado |
| `python main.py --bug 2` | Testa com o BUG 2 ligado |
| `python main.py --comparar` | Roda sem bug e com o BUG 1 e compara |
| `python main.py --comparar --bug 2` | Mesma comparação com o BUG 2 |

Com `--abrir` o relatório abre no navegador no final. No VS Code também dá para rodar com F5.

Os resultados ficam na pasta `relatorios/`: o relatório `relatorio_qa.html`, o resultado de cada teste em `resultados_testes.csv` e o histórico das execuções em `historico_execucoes.csv`.

## Pastas

- `sistema/cinema.py`: o sistema testado
- `testes/`: os casos de teste e o executor
- `qa/`: métricas, decisão, CSV, terminal e relatório HTML
- `dados/`: requisitos e sessões usadas nos testes

## Requisitos

| Requisito | Regra |
|---|---|
| RF01 Venda | Um assento livre e existente pode ser vendido e fica ocupado. |
| RF02 Assento único | Um assento vendido não pode ser vendido de novo na mesma sessão. |
| RF03 Meia-entrada | Estudantes e pessoas com 60 anos ou mais pagam metade. |
| RF04 Classificação | O cliente precisa ter a idade mínima do filme. |
| RF05 Cancelamento | Um ingresso pode ser cancelado e o assento fica livre. |

## Casos de teste

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

Cada teste roda com um cinema novo, para um não atrapalhar o outro.

## Decisão de QA

- LIBERADO: nenhum teste falhou.
- LIBERADO COM RESSALVAS: teve falha, mas nenhuma crítica.
- NÃO LIBERAR: teve pelo menos uma falha crítica.

## Bugs propositais

Os dois bugs ficam em `sistema/cinema.py`, marcados com `# BUG PROPOSITAL`, e começam desligados.

| | BUG 1 | BUG 2 |
|---|---|---|
| O que faz | Vende o mesmo assento duas vezes | Quem tem 60 anos paga inteira (`>` no lugar de `>=`) |
| Teste que pega | CT04 | CT07 |
| Decisão | NÃO LIBERAR | LIBERADO COM RESSALVAS |

Nos dois casos a taxa de aprovação é 91,7%, mas a decisão muda porque o BUG 1 é crítico e o BUG 2 não.
