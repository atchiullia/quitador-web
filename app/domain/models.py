from dataclasses import dataclass

@dataclass
class Emprestimo:
    nome: str
    saldo: float
    parcela: float
    juros_mensal: float  # as percent, will be converted in __post_init__
    entra_no_aporte: bool = True
    pago: bool = False

    def __post_init__(self):
        self.juros_mensal = self.juros_mensal / 100
