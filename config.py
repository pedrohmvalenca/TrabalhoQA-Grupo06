from pathlib import Path

NOME_DO_SISTEMA = "Bilheteria de Cinema"

EQUIPE = "Pedro Valença, Jorge Antônio, Nicolas Tavares, Ygor Sampaio e Davi Felipe"

PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_DADOS = PASTA_PROJETO / "dados"
PASTA_RELATORIOS = PASTA_PROJETO / "relatorios"

ARQUIVO_REQUISITOS = PASTA_DADOS / "requisitos.json"
ARQUIVO_SESSOES = PASTA_DADOS / "sessoes.json"

RELATORIO_HTML = PASTA_RELATORIOS / "relatorio_qa.html"
RESULTADOS_CSV = PASTA_RELATORIOS / "resultados_testes.csv"
HISTORICO_CSV = PASTA_RELATORIOS / "historico_execucoes.csv"
