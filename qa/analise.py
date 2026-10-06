import json
from datetime import datetime

import config
from testes.casos_de_teste import CRITICA, ALTA, MEDIA, BAIXA

LIBERADO = "LIBERADO"
LIBERADO_COM_RESSALVAS = "LIBERADO COM RESSALVAS"
NAO_LIBERAR = "NÃO LIBERAR"

ORDEM_DE_GRAVIDADE = [CRITICA, ALTA, MEDIA, BAIXA]


def analisar_execucao(cenario, resultados):
    defeitos = []
    for severidade in ORDEM_DE_GRAVIDADE:
        for resultado in resultados:
            if resultado["situacao"] == "FAIL" and resultado["severidade"] == severidade:
                defeitos.append(resultado)

    numero = 1
    for defeito in defeitos:
        defeito["codigo_defeito"] = "DEF-" + str(numero).zfill(2)
        numero = numero + 1

    falhas_criticas = 0
    for defeito in defeitos:
        if defeito["severidade"] == CRITICA:
            falhas_criticas = falhas_criticas + 1

    total = len(resultados)
    reprovados = len(defeitos)
    aprovados = total - reprovados
    taxa = aprovados / total * 100

    decisao, motivo = decidir(reprovados, falhas_criticas)

    return {
        "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "cenario": cenario,
        "resultados": resultados,
        "total": total,
        "aprovados": aprovados,
        "reprovados": reprovados,
        "taxa_aprovacao": f"{taxa:.1f}".replace(".", ","),
        "falhas_criticas": falhas_criticas,
        "defeitos": defeitos,
        "decisao": decisao,
        "motivo": motivo,
        "comparacao": [],
    }


def decidir(reprovados, falhas_criticas):
    if reprovados == 0:
        return LIBERADO, "Todos os testes passaram."

    if falhas_criticas == 0:
        if reprovados == 1:
            quantidade = "1 teste falhou"
        else:
            quantidade = str(reprovados) + " testes falharam"
        return LIBERADO_COM_RESSALVAS, quantidade + ", mas nenhuma falha é crítica. Corrigir na próxima versão."

    if falhas_criticas == 1:
        quantidade = "1 falha crítica"
    else:
        quantidade = str(falhas_criticas) + " falhas críticas"
    return NAO_LIBERAR, quantidade + ": a versão não pode ser liberada."


def carregar_requisitos():
    with open(config.ARQUIVO_REQUISITOS, encoding="utf-8") as arquivo:
        return json.load(arquivo)


def resumo_por_requisito(resultados):
    resumo = []
    for requisito in carregar_requisitos():
        testes = 0
        reprovados = 0
        for resultado in resultados:
            if resultado["requisito"] == requisito["id"]:
                testes = testes + 1
                if resultado["situacao"] == "FAIL":
                    reprovados = reprovados + 1
        resumo.append({
            "id": requisito["id"],
            "nome": requisito["nome"],
            "regra": requisito["regra"],
            "testes": testes,
            "aprovados": testes - reprovados,
            "reprovados": reprovados,
        })
    return resumo
