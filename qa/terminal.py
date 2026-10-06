import config

LARGURA = 86


def titulo(texto):
    print()
    print(texto)
    print("-" * LARGURA)


def faixa(texto):
    print()
    print("#" * LARGURA)
    print(" " + texto)
    print("#" * LARGURA)


def mostrar_execucao(execucao):
    print()
    print("=" * LARGURA)
    print(" QA - " + config.NOME_DO_SISTEMA)
    print(" Cenário : " + execucao["cenario"])
    print(" Execução: " + execucao["data_hora"])
    print("=" * LARGURA)

    titulo("CASOS DE TESTE")
    for resultado in execucao["resultados"]:
        pontos = "." * (63 - len(resultado["descricao"]))
        linha = " " + resultado["id"] + "  " + resultado["requisito"] + "  " + resultado["descricao"]
        print(linha + " " + pontos + " " + resultado["situacao"])
        if resultado["situacao"] == "FAIL":
            print("             esperado  : " + resultado["esperado"])
            print("             obtido    : " + resultado["obtido"])
            print("             severidade: " + resultado["severidade"])

    titulo("MÉTRICAS DE QUALIDADE")
    print(" Testes executados ........ " + str(execucao["total"]))
    print(" Aprovados (PASS) ......... " + str(execucao["aprovados"]))
    print(" Reprovados (FAIL) ........ " + str(execucao["reprovados"]))
    print(" Taxa de aprovação ........ " + execucao["taxa_aprovacao"] + "%")
    print(" Falhas críticas .......... " + str(execucao["falhas_criticas"]))

    titulo("DEFEITOS ENCONTRADOS")
    if len(execucao["defeitos"]) == 0:
        print(" Nenhum defeito encontrado.")
    for defeito in execucao["defeitos"]:
        print(" " + defeito["codigo_defeito"] + "  [" + defeito["severidade"] + "]  "
              + defeito["id"] + " / " + defeito["requisito"] + ": " + defeito["descricao"])

    print()
    print("=" * LARGURA)
    print(" DECISÃO FINAL DE QA: " + execucao["decisao"])
    print(" " + execucao["motivo"])
    print("=" * LARGURA)

    if len(execucao["comparacao"]) > 0:
        mostrar_comparacao(execucao["comparacao"])


def mostrar_comparacao(comparacao):
    titulo("ANTES x DEPOIS  (execução anterior x execução atual)")
    algum_mudou = False
    for linha in comparacao:
        texto = " " + linha["indicador"] + ": " + linha["antes"] + "  ->  " + linha["depois"]
        if linha["mudou"]:
            texto = texto + "  <- mudou"
            algum_mudou = True
        print(texto)
    if not algum_mudou:
        print(" Nenhum indicador mudou em relação à execução anterior.")


def mostrar_arquivos(gerados, nao_gravados):
    titulo("ARQUIVOS GERADOS")
    for caminho in gerados:
        print(" " + str(caminho.relative_to(config.PASTA_PROJETO)))
    for caminho in nao_gravados:
        print(" AVISO: não consegui gravar " + caminho.name + ". Feche o arquivo se ele estiver aberto e execute de novo.")
    print()
