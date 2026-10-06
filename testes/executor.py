import json

import config
from sistema.cinema import Cinema, ErroDeNegocio
from testes.casos_de_teste import CASOS_DE_TESTE


def carregar_sessoes():
    with open(config.ARQUIVO_SESSOES, encoding="utf-8") as arquivo:
        return json.load(arquivo)


def executar_testes(bug):
    resultados = []
    for caso in CASOS_DE_TESTE:
        cinema = Cinema(carregar_sessoes(), bug_1_assento_duplicado=(bug == 1), bug_2_meia_aos_60=(bug == 2))
        passos = caso["funcao"]

        try:
            obtido = passos(cinema)
        except ErroDeNegocio as erro:
            obtido = "Recusado: " + str(erro)
        except Exception as erro:
            obtido = "ERRO INESPERADO: " + type(erro).__name__ + ": " + str(erro)

        if obtido == caso["esperado"]:
            situacao = "PASS"
            severidade = "-"
        else:
            situacao = "FAIL"
            severidade = caso["severidade"]

        resultados.append({
            "id": caso["id"],
            "requisito": caso["requisito"],
            "tipo": caso["tipo"],
            "descricao": caso["descricao"],
            "esperado": caso["esperado"],
            "obtido": obtido,
            "situacao": situacao,
            "severidade": severidade,
        })
    return resultados
