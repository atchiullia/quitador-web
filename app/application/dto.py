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


class SimulacaoSnowballRequest:
    def __init__(self, nomes: list, saldos: list, parcelas: list, juros: list, 
                 aporte_fixo: float, aporte_extra: float):
        self.nomes = nomes
        self.saldos = saldos
        self.parcelas = parcelas
        self.juros = juros
        self.aporte_fixo = aporte_fixo
        self.aporte_extra = aporte_extra
    
    @classmethod
    def from_form_data(cls, form_data):
        return cls(
            nomes=form_data.getlist('nome[]'),
            saldos=form_data.getlist('saldo[]'),
            parcelas=form_data.getlist('parcela[]'),
            juros=form_data.getlist('juros[]'),
            aporte_fixo=float(form_data.get('aporte_fixo', 0)),
            aporte_extra=float(form_data.get('aporte_extra', 0))
        )
    
    def validate(self):
        errors = []
        
        if not self.nomes or len(self.nomes) == 0:
            errors.append("Adicione pelo menos um empréstimo")
            return errors
        
        for i, (nome, saldo, parcela, juro) in enumerate(zip(self.nomes, self.saldos, self.parcelas, self.juros)):
            if not nome.strip():
                errors.append(f"Empréstimo {i+1}: Nome é obrigatório")
            
            try:
                saldo_val = float(saldo)
                if saldo_val <= 0:
                    errors.append(f"Empréstimo {i+1}: Saldo deve ser maior que zero")
                if saldo_val > 10000000:
                    errors.append(f"Empréstimo {i+1}: Saldo máximo é R$ 10.000.000,00")
            except ValueError:
                errors.append(f"Empréstimo {i+1}: Saldo inválido")
            
            try:
                parcela_val = float(parcela)
                if parcela_val <= 0:
                    errors.append(f"Empréstimo {i+1}: Parcela deve ser maior que zero")
                if parcela_val > 1000000:
                    errors.append(f"Empréstimo {i+1}: Parcela máxima é R$ 1.000.000,00")
            except ValueError:
                errors.append(f"Empréstimo {i+1}: Parcela inválida")
            
            try:
                juro_val = float(juro)
                if juro_val <= 0:
                    errors.append(f"Empréstimo {i+1}: Juros devem ser maiores que zero")
                if juro_val > 50:
                    errors.append(f"Empréstimo {i+1}: Juros máximos são 50% ao mês")
            except ValueError:
                errors.append(f"Empréstimo {i+1}: Juros inválidos")
        
        if self.aporte_fixo < 0:
            errors.append("Aporte fixo não pode ser negativo")
        if self.aporte_fixo > 1000000:
            errors.append("Aporte fixo máximo é R$ 1.000.000,00")
        
        if self.aporte_extra < 0:
            errors.append("Aporte extra não pode ser negativo")
        if self.aporte_extra > 1000000:
            errors.append("Aporte extra máximo é R$ 1.000.000,00")
        
        return errors


