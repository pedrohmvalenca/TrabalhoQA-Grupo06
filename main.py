import argparse
import webbrowser

import config
from qa import analise, registros, relatorio_html, terminal
from testes.executor import executar_testes


def ler_argumentos():
    leitor = argparse.ArgumentParser(description="Automação de QA da Bilheteria de Cinema")
    leitor.add_argument("--bug", type=int, choices=[1, 2], default=0,
                        help="liga um bug proposital: 1 = assento duplicado (crítico), "
                             "2 = meia-entrada aos 60 anos (não crítico)")
    leitor.add_argument("--comparar", action="store_true",
                        help="executa sem bug e depois com bug, e compara o antes e o depois")
    leitor.add_argument("--abrir", action="store_true",
                        help="abre o relatório HTML no navegador ao final")
    return leitor.parse_args()


def descrever_cenario(bug):
    if bug == 1:
        return "Com BUG 1 (assento duplicado)"
    if bug == 2:
        return "Com BUG 2 (meia aos 60 anos)"
    return "Sistema original (sem bug)"


def executar_qa(bug, comparar_com_anterior):
    resultados = executar_testes(bug)
    execucao = analise.analisar_execucao(descrever_cenario(bug), resultados)

    if comparar_com_anterior:
        anterior = registros.ler_execucao_anterior()
        if anterior is not None:
            execucao["comparacao"] = registros.comparar(anterior, execucao)

    terminal.mostrar_execucao(execucao)

    config.PASTA_RELATORIOS.mkdir(exist_ok=True)
    relatorio_html.gerar(execucao)
    gerados = [config.RELATORIO_HTML]
    nao_gravados = []

    try:
        registros.salvar_resultados(execucao)
        gerados.append(config.RESULTADOS_CSV)
    except PermissionError:
        nao_gravados.append(config.RESULTADOS_CSV)

    try:
        registros.registrar_no_historico(execucao)
        gerados.append(config.HISTORICO_CSV)
    except PermissionError:
        nao_gravados.append(config.HISTORICO_CSV)

    terminal.mostrar_arquivos(gerados, nao_gravados)


def main():
    argumentos = ler_argumentos()

    if argumentos.comparar:
        bug_depois = argumentos.bug
        if bug_depois == 0:
            bug_depois = 1

        terminal.faixa("ANTES: sistema original")
        executar_qa(0, False)

        terminal.faixa("DEPOIS: com o bug proposital")
        executar_qa(bug_depois, True)
    else:
        executar_qa(argumentos.bug, True)

    if argumentos.abrir:
        webbrowser.open(config.RELATORIO_HTML.as_uri())


if __name__ == "__main__":
    main()
