from string import Template

import config
from qa.analise import LIBERADO, LIBERADO_COM_RESSALVAS, NAO_LIBERAR, resumo_por_requisito
from testes.casos_de_teste import CRITICA, ALTA, MEDIA, BAIXA

MODELO = config.PASTA_PROJETO / "qa" / "modelo_relatorio.html"

CLASSE_DA_DECISAO = {
    LIBERADO: "liberado",
    LIBERADO_COM_RESSALVAS: "ressalvas",
    NAO_LIBERAR: "nao-liberar",
}

CLASSE_DA_SEVERIDADE = {
    CRITICA: "critica",
    ALTA: "alta",
    MEDIA: "media",
    BAIXA: "baixa",
}


def gerar(execucao):
    requisitos = resumo_por_requisito(execucao["resultados"])

    equipe = ""
    if config.EQUIPE.strip() != "":
        equipe = "<tr><th>Equipe</th><td>" + config.EQUIPE + "</td></tr>"

    with open(MODELO, encoding="utf-8") as arquivo:
        modelo = Template(arquivo.read())

    pagina = modelo.substitute(
        sistema=config.NOME_DO_SISTEMA,
        equipe=equipe,
        cenario=execucao["cenario"],
        data_hora=execucao["data_hora"],
        decisao=execucao["decisao"],
        classe_decisao=CLASSE_DA_DECISAO[execucao["decisao"]],
        motivo=execucao["motivo"],
        total=execucao["total"],
        aprovados=execucao["aprovados"],
        reprovados=execucao["reprovados"],
        taxa=execucao["taxa_aprovacao"],
        criticas=execucao["falhas_criticas"],
        comparacao=montar_comparacao(execucao["comparacao"]),
        defeitos=montar_defeitos(execucao["defeitos"], requisitos),
        requisitos=montar_requisitos(requisitos),
        testes=montar_testes(execucao["resultados"]),
    )

    with open(config.RELATORIO_HTML, "w", encoding="utf-8") as arquivo:
        arquivo.write(pagina)


def selo(texto, classe):
    return f'<span class="selo {classe}">{texto}</span>'


def selo_da_severidade(severidade):
    if severidade == "-":
        return "-"
    return selo(severidade, CLASSE_DA_SEVERIDADE[severidade])


def montar_testes(resultados):
    linhas = ""
    for resultado in resultados:
        if resultado["situacao"] == "PASS":
            linhas = linhas + f'<tr id="{resultado["id"]}">'
            situacao = selo("PASS", "pass")
        else:
            linhas = linhas + f'<tr id="{resultado["id"]}" class="falhou">'
            situacao = selo("FAIL", "fail")
        linhas = linhas + f'<td>{resultado["id"]}</td>'
        linhas = linhas + f'<td>{resultado["requisito"]}</td>'
        linhas = linhas + f'<td>{resultado["descricao"]}<small>{resultado["tipo"]}</small></td>'
        linhas = linhas + f'<td>{resultado["esperado"]}</td>'
        linhas = linhas + f'<td>{resultado["obtido"]}</td>'
        linhas = linhas + f'<td>{situacao}</td>'
        linhas = linhas + f'<td>{selo_da_severidade(resultado["severidade"])}</td>'
        linhas = linhas + "</tr>\n"
    return linhas


def montar_requisitos(requisitos):
    linhas = ""
    for requisito in requisitos:
        if requisito["testes"] == 0:
            situacao = selo("Sem testes", "ressalvas")
        elif requisito["reprovados"] > 0:
            situacao = selo("Com defeito", "fail")
        else:
            situacao = selo("Sem defeitos", "pass")

        if requisito["reprovados"] > 0:
            linhas = linhas + '<tr class="falhou">'
        else:
            linhas = linhas + "<tr>"
        linhas = linhas + f'<td>{requisito["id"]}</td>'
        linhas = linhas + f'<td><b>{requisito["nome"]}</b><small>{requisito["regra"]}</small></td>'
        linhas = linhas + f'<td>{requisito["testes"]}</td>'
        linhas = linhas + f'<td>{requisito["aprovados"]}</td>'
        linhas = linhas + f'<td>{requisito["reprovados"]}</td>'
        linhas = linhas + f'<td>{situacao}</td>'
        linhas = linhas + "</tr>\n"
    return linhas


def montar_defeitos(defeitos, requisitos):
    if len(defeitos) == 0:
        return "<p>Nenhum defeito encontrado: todos os testes tiveram o resultado esperado.</p>"

    linhas = ""
    for defeito in defeitos:
        nome_do_requisito = ""
        for requisito in requisitos:
            if requisito["id"] == defeito["requisito"]:
                nome_do_requisito = requisito["nome"]

        linhas = linhas + '<tr class="falhou">'
        linhas = linhas + f'<td>{defeito["codigo_defeito"]}</td>'
        linhas = linhas + f'<td>{selo_da_severidade(defeito["severidade"])}</td>'
        linhas = linhas + f'<td><a href="#{defeito["id"]}"><b>{defeito["id"]}</b></a><small>{defeito["descricao"]}</small></td>'
        linhas = linhas + f'<td><b>{defeito["requisito"]}</b><small>{nome_do_requisito}</small></td>'
        linhas = linhas + f'<td>{defeito["esperado"]}</td>'
        linhas = linhas + f'<td>{defeito["obtido"]}</td>'
        linhas = linhas + "</tr>\n"

    return (
        "<p>Cada teste reprovado é registrado como um defeito, do mais grave para o menos grave.</p>\n"
        "<table>\n"
        "<tr><th>Defeito</th><th>Severidade</th><th>Teste que falhou</th>"
        "<th>Regra de negócio</th><th>Resultado esperado</th><th>Resultado obtido</th></tr>\n"
        + linhas
        + "</table>"
    )


def montar_comparacao(comparacao):
    if len(comparacao) == 0:
        return ""

    linhas = ""
    algum_mudou = False
    for linha in comparacao:
        antes = linha["antes"]
        depois = linha["depois"]
        if linha["indicador"] == "Decisão de QA":
            antes = selo(antes, CLASSE_DA_DECISAO[antes])
            depois = selo(depois, CLASSE_DA_DECISAO[depois])

        if linha["mudou"]:
            linhas = linhas + '<tr class="mudou">'
            algum_mudou = True
        else:
            linhas = linhas + "<tr>"
        linhas = linhas + f'<td>{linha["indicador"]}</td><td>{antes}</td><td>{depois}</td></tr>\n'

    if algum_mudou:
        observacao = "As linhas destacadas são os indicadores que mudaram."
    else:
        observacao = "Nenhum indicador mudou."

    return (
        "<h2>Antes e depois</h2>\n"
        f"<p>Comparação entre a execução anterior e a execução atual. {observacao}</p>\n"
        "<table>\n"
        "<tr><th>Indicador</th><th>Antes (execução anterior)</th><th>Depois (execução atual)</th></tr>\n"
        + linhas
        + "</table>"
    )
