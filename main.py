from enum import Enum
from typing import List


class Local(Enum):
    Nordeste = 'NE'
    Norte = 'NO'
    Sudeste = 'SE'
    Sul = 'SU'
    Centro_oeste = 'CO'


class Cliente():

    def __init__(self, nome, fidelidade, cpf,local: Local):
        self.nome = nome
        self.fidelidade = bool(fidelidade)
        self.cpf = cpf
        self.local = local

class Produto():

    def __init__(self, nome, valor, ctg):
        self.nome = nome
        self.valor = valor
        self.ctg = ctg


class ItemCompra():

    def __init__(self, produto: Produto, qtd: int):
        self.produto = produto
        self.qtd = qtd


class Compra():

    def __init__(self, cliente: Cliente, itens: List[ItemCompra]):
        self.itens = itens
        self.cliente = cliente

    @property
    def valor_total(self) -> float:
        return sum([item.produto.valor * item.qtd for item in self.itens])


class Promocao():

    def aplicavel(self, compra: Compra) -> bool:
        raise NotImplemented('Abstratata')

    def calcular_desconto(self, compra: Compra) -> float:
        raise NotImplemented('Abstrata')

    def desconto(self, compra) -> float:
        return self.calcular_desconto(compra) if self.aplicavel(compra) else 0.0


class PromocaoPontoFidelidade(Promocao):

    def aplicavel(self, compra: Compra) -> bool:
        return True if compra.cliente.fidelidade == True else False

    def calcular_desconto(self, compra: Compra) -> float:
        desconto = 0.0
        if (compra.valor_total > 99):
            desconto = compra.valor_total * 0.05
        elif(compra.valor_total >999):
            desconto = compra.valor_total * 0.1
        return desconto


class PromocaoLeveEPague(Promocao):

    def aplicavel(self, compra: Compra) -> bool:
        return True if compra.itens.qtd == 3 else False

    def calcular_desconto(self, compra: Compra) ->float:
        return compra.valor_total * 0.33


class AplicadorDesconto():

    def __init__(self, compra: Compra, promocoes: List[Promocao]):
        self.compra = compra
        self.promocoes = promocoes

    def valor_final(self) -> float:
        return self.compra.valor_total - self.valor_descontos()

    def valor_descontos(self) -> float:
        return sum([p.desconto(self.compra) for p in self.promocoes])


class Frete():

    def aplicavel(self, compra: Compra) -> bool:
        raise NotImplemented('Abstrata')

    def calcular_frete(self, compra: Compra) -> float:
        raise NotImplemented('Abstrata')

    def frete(self, compra) -> float:
        return self.calcular_frete(compra) if self.aplicavel(compra) else 0.0

class FreteGratis(Frete):

    def aplicavel(self, compra: Compra) -> bool:
        return True if compra.valor_total == 199 else False

    def calcular_frete(self, compra: Compra) -> float:
        return compra.valor_total


class FreteSeSE(Frete):

    def aplicavel(self, compra: Compra) -> bool:
        res = False
        if (compra.valor_total > 99):
            if(compra.cliente.local.Sudeste | compra.cliente.local.Sul):
                res = True
            else:
                res = False
        return res

    def calcular_frete(self, compra: Compra) -> float:
        return compra.valor_total


class FreteFixo(Frete):

    def aplicavel(self, compra: Compra) -> bool:
        res = False
        if compra.valor_total <= 99:
            res = True
        else:
            res = False
        return res

    def calcular_frete(self, compra: Compra):
        return compra.valor_total * 0.1


class CobrarFrete():

    def __init__(self, compra: Compra, fretes: List[Frete]):
        self.compra = compra
        self.fretes = fretes

    def valor_final(self) -> float:
        return self.compra.valor_total + self.valor_cobrado()

    def valor_cobrado(self) -> float:
        return sum([f.frete(self.compra) for f in self.fretes])
