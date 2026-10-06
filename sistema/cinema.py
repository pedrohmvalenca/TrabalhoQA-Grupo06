"""
SISTEMA EM TESTE - Bilheteria de Cinema
=======================================
Este arquivo é o "produto" que o QA avalia. Ele é pequeno de propósito:
o foco do trabalho é o processo de qualidade, não o tamanho do sistema.

Regras de negócio (as mesmas de dados/requisitos.json):
    RF01  Venda de ingresso ......... um assento livre da sala pode ser vendido
    RF02  Assento único ............. um assento já vendido não pode ser vendido de novo
    RF03  Meia-entrada .............. estudante e idoso (60 anos ou mais) pagam 50%
    RF04  Classificação indicativa .. o cliente precisa ter a idade mínima do filme
    RF05  Cancelamento .............. o ingresso cancelado libera o assento
"""

IDADE_IDOSO = 60
DESCONTO_MEIA = 0.5


class ErroDeNegocio(Exception):
    pass


class Cinema:
    def __init__(self, sessoes, bug_1_assento_duplicado=False, bug_2_meia_aos_60=False):
        self.bug_1_assento_duplicado = bug_1_assento_duplicado
        self.bug_2_meia_aos_60 = bug_2_meia_aos_60
        self.sessoes = {}
        self.ocupados = {}
        for sessao in sessoes:
            self.sessoes[sessao["id"]] = sessao
            self.ocupados[sessao["id"]] = set()
        self.ingressos = {}
        self.proximo_codigo = 1

    def buscar_sessao(self, sessao_id):
        if sessao_id not in self.sessoes:
            raise ErroDeNegocio("sessão não encontrada")
        return self.sessoes[sessao_id]

    def assento_livre(self, sessao_id, assento):
        self.buscar_sessao(sessao_id)
        return assento not in self.ocupados[sessao_id]

    def calcular_preco(self, sessao_id, idade, estudante=False):
        sessao = self.buscar_sessao(sessao_id)

        if self.bug_2_meia_aos_60:
            idoso = idade > IDADE_IDOSO     # BUG PROPOSITAL: ">" no lugar de ">="
        else:
            idoso = idade >= IDADE_IDOSO

        if estudante or idoso:
            return round(sessao["preco"] * DESCONTO_MEIA, 2)
        return sessao["preco"]

    def vender_ingresso(self, sessao_id, assento, idade, estudante=False):
        sessao = self.buscar_sessao(sessao_id)

        if assento not in sessao["assentos"]:
            raise ErroDeNegocio("assento inexistente")

        if idade < sessao["classificacao"]:
            raise ErroDeNegocio("idade abaixo da classificação indicativa")

        if not self.bug_1_assento_duplicado:     # BUG PROPOSITAL: ligado, pula esta validação
            if assento in self.ocupados[sessao_id]:
                raise ErroDeNegocio("assento já vendido")

        ingresso = {
            "codigo": self.proximo_codigo,
            "sessao": sessao_id,
            "assento": assento,
            "preco": self.calcular_preco(sessao_id, idade, estudante),
        }
        self.ingressos[ingresso["codigo"]] = ingresso
        self.ocupados[sessao_id].add(assento)
        self.proximo_codigo += 1
        return ingresso

    def cancelar_ingresso(self, codigo):
        if codigo not in self.ingressos:
            raise ErroDeNegocio("ingresso não encontrado")
        ingresso = self.ingressos.pop(codigo)
        self.ocupados[ingresso["sessao"]].discard(ingresso["assento"])
        return ingresso
