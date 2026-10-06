import csv

import config

COLUNAS_DOS_RESULTADOS = [
    "ID", "Requisito", "Tipo de cenário", "Descrição", "Resultado esperado",
    "Resultado obtido", "Situação", "Severidade", "Data/Hora", "Cenário",
]

COLUNAS_DO_HISTORICO = [
    "Data/Hora", "Cenário", "Testes executados", "Aprovados", "Reprovados",
    "Taxa de aprovação (%)", "Falhas críticas", "Decisão de QA", "Testes reprovados",
]


def salvar_resultados(execucao):
    with open(config.RESULTADOS_CSV, "w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(COLUNAS_DOS_RESULTADOS)
        for resultado in execucao["resultados"]:
            escritor.writerow([
                resultado["id"],
                resultado["requisito"],
                resultado["tipo"],
                resultado["descricao"],
                resultado["esperado"],
                resultado["obtido"],
                resultado["situacao"],
                resultado["severidade"],
                execucao["data_hora"],
                execucao["cenario"],
            ])


def linha_do_historico(execucao):
    ids_reprovados = []
    for defeito in execucao["defeitos"]:
        ids_reprovados.append(defeito["id"])
    testes_reprovados = " ".join(ids_reprovados)
    if testes_reprovados == "":
        testes_reprovados = "nenhum"

    return {
        "Data/Hora": execucao["data_hora"],
        "Cenário": execucao["cenario"],
        "Testes executados": str(execucao["total"]),
        "Aprovados": str(execucao["aprovados"]),
        "Reprovados": str(execucao["reprovados"]),
        "Taxa de aprovação (%)": execucao["taxa_aprovacao"],
        "Falhas críticas": str(execucao["falhas_criticas"]),
        "Decisão de QA": execucao["decisao"],
        "Testes reprovados": testes_reprovados,
    }


def registrar_no_historico(execucao):
    arquivo_ja_existe = config.HISTORICO_CSV.exists()
    with open(config.HISTORICO_CSV, "a", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS_DO_HISTORICO, delimiter=";")
        if not arquivo_ja_existe:
            escritor.writeheader()
        escritor.writerow(linha_do_historico(execucao))


def ler_execucao_anterior():
    if not config.HISTORICO_CSV.exists():
        return None

    with open(config.HISTORICO_CSV, newline="", encoding="utf-8-sig") as arquivo:
        linhas = list(csv.DictReader(arquivo, delimiter=";"))

    if len(linhas) == 0:
        return None
    return linhas[-1]


def comparar(anterior, execucao):
    atual = linha_do_historico(execucao)
    tabela = []
    for coluna in COLUNAS_DO_HISTORICO:
        antes = anterior[coluna]
        depois = atual[coluna]
        mudou = False
        if antes != depois and coluna != "Data/Hora" and coluna != "Cenário":
            mudou = True
        tabela.append({
            "indicador": coluna,
            "antes": antes,
            "depois": depois,
            "mudou": mudou,
        })
    return tabela
