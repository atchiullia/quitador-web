class Emprestimo:
    def __init__(self, nome, saldo, parcela, juros_mensal, entra_no_aporte=True):
        self.nome = nome
        self.saldo = saldo
        self.parcela = parcela
        self.juros_mensal = juros_mensal / 100  # converte de percentual
        self.entra_no_aporte = entra_no_aporte
        self.pago = False
