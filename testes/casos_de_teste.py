CRITICA = "CRÍTICA"
ALTA = "ALTA"
MEDIA = "MÉDIA"
BAIXA = "BAIXA"

NORMAL = "Cenário normal"
ERRO = "Cenário de erro"
LIMITE = "Valor limite"


def reais(valor):
    return "R$ " + f"{valor:.2f}".replace(".", ",")


def ct01(cinema):
    cinema.vender_ingresso("S1", "A1", idade=30)
    if cinema.assento_livre("S1", "A1"):
        return "Ingresso emitido; assento A1 livre"
    return "Ingresso emitido; assento A1 ocupado"


def ct02(cinema):
    cinema.vender_ingresso("S1", "Z99", idade=30)
    return "Ingresso emitido"


def ct03(cinema):
    cinema.vender_ingresso("S1", "A1", idade=30)
    cinema.vender_ingresso("S1", "A2", idade=30)
    return str(len(cinema.ingressos)) + " ingressos emitidos"


def ct04(cinema):
    cinema.vender_ingresso("S1", "A1", idade=30)
    cinema.vender_ingresso("S1", "A1", idade=25)
    return "Ingresso emitido"


def ct05(cinema):
    ingresso = cinema.vender_ingresso("S1", "A1", idade=30)
    return "Preço cobrado: " + reais(ingresso["preco"])


def ct06(cinema):
    ingresso = cinema.vender_ingresso("S1", "A1", idade=20, estudante=True)
    return "Preço cobrado: " + reais(ingresso["preco"])


def ct07(cinema):
    ingresso = cinema.vender_ingresso("S1", "A1", idade=60)
    return "Preço cobrado: " + reais(ingresso["preco"])


def ct08(cinema):
    cinema.vender_ingresso("S2", "A1", idade=18)
    return "Ingresso emitido"


def ct09(cinema):
    cinema.vender_ingresso("S2", "A1", idade=15)
    return "Ingresso emitido"


def ct10(cinema):
    cinema.vender_ingresso("S2", "A1", idade=16)
    return "Ingresso emitido"


def ct11(cinema):
    ingresso = cinema.vender_ingresso("S1", "A1", idade=30)
    cinema.cancelar_ingresso(ingresso["codigo"])
    if cinema.assento_livre("S1", "A1"):
        return "Ingresso cancelado; assento A1 livre"
    return "Ingresso cancelado; assento A1 ocupado"


def ct12(cinema):
    cinema.cancelar_ingresso(999)
    return "Ingresso cancelado"


CASOS_DE_TESTE = [
    {
        "id": "CT01",
        "requisito": "RF01",
        "tipo": NORMAL,
        "descricao": "Vender ingresso para um assento livre",
        "esperado": "Ingresso emitido; assento A1 ocupado",
        "severidade": CRITICA,
        "funcao": ct01,
    },
    {
        "id": "CT02",
        "requisito": "RF01",
        "tipo": ERRO,
        "descricao": "Tentar vender um assento que não existe na sala",
        "esperado": "Recusado: assento inexistente",
        "severidade": MEDIA,
        "funcao": ct02,
    },
    {
        "id": "CT03",
        "requisito": "RF02",
        "tipo": NORMAL,
        "descricao": "Vender dois assentos diferentes na mesma sessão",
        "esperado": "2 ingressos emitidos",
        "severidade": ALTA,
        "funcao": ct03,
    },
    {
        "id": "CT04",
        "requisito": "RF02",
        "tipo": ERRO,
        "descricao": "Tentar vender o mesmo assento pela segunda vez",
        "esperado": "Recusado: assento já vendido",
        "severidade": CRITICA,
        "funcao": ct04,
    },
    {
        "id": "CT05",
        "requisito": "RF03",
        "tipo": NORMAL,
        "descricao": "Adulto sem benefício paga o ingresso inteiro",
        "esperado": "Preço cobrado: R$ 30,00",
        "severidade": ALTA,
        "funcao": ct05,
    },
    {
        "id": "CT06",
        "requisito": "RF03",
        "tipo": NORMAL,
        "descricao": "Estudante paga meia-entrada",
        "esperado": "Preço cobrado: R$ 15,00",
        "severidade": ALTA,
        "funcao": ct06,
    },
    {
        "id": "CT07",
        "requisito": "RF03",
        "tipo": LIMITE,
        "descricao": "Cliente com exatamente 60 anos paga meia-entrada",
        "esperado": "Preço cobrado: R$ 15,00",
        "severidade": MEDIA,
        "funcao": ct07,
    },
    {
        "id": "CT08",
        "requisito": "RF04",
        "tipo": NORMAL,
        "descricao": "Cliente de 18 anos compra ingresso de filme 16 anos",
        "esperado": "Ingresso emitido",
        "severidade": ALTA,
        "funcao": ct08,
    },
    {
        "id": "CT09",
        "requisito": "RF04",
        "tipo": ERRO,
        "descricao": "Cliente de 15 anos tenta comprar ingresso de filme 16 anos",
        "esperado": "Recusado: idade abaixo da classificação indicativa",
        "severidade": CRITICA,
        "funcao": ct09,
    },
    {
        "id": "CT10",
        "requisito": "RF04",
        "tipo": LIMITE,
        "descricao": "Cliente com exatamente 16 anos compra filme 16 anos",
        "esperado": "Ingresso emitido",
        "severidade": MEDIA,
        "funcao": ct10,
    },
    {
        "id": "CT11",
        "requisito": "RF05",
        "tipo": NORMAL,
        "descricao": "Cancelar um ingresso e conferir se o assento foi liberado",
        "esperado": "Ingresso cancelado; assento A1 livre",
        "severidade": ALTA,
        "funcao": ct11,
    },
    {
        "id": "CT12",
        "requisito": "RF05",
        "tipo": ERRO,
        "descricao": "Tentar cancelar um ingresso que não existe",
        "esperado": "Recusado: ingresso não encontrado",
        "severidade": BAIXA,
        "funcao": ct12,
    },
]
