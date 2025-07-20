from dataclasses import dataclass
from typing import List

@dataclass
class EmprestimoDTO:
    nome: str
    saldo: float
    parcela: float
    juros_mensal: float
    entra_no_aporte: bool = True

@dataclass
class SimulacaoRequestDTO:
    emprestimos: List[EmprestimoDTO]
    aporte_fixo: float
    aporte_extra: float = 0
    meses_maximos: int = 120

@dataclass
class SimulacaoResponseDTO:
    resultado: dict


