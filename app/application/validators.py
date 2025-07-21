from pydantic import BaseModel, validator
from typing import List
from decimal import Decimal

class EmprestimoValidator(BaseModel):
    nome: str
    saldo: Decimal
    parcela: Decimal
    juros: Decimal
    
    @validator('nome')
    def nome_deve_ter_conteudo(cls, v):
        if not v.strip():
            raise ValueError('Nome é obrigatório')
        if len(v) > 50:
            raise ValueError('Nome máximo 50 caracteres')
        return v.strip()
    
    @validator('saldo', 'parcela', 'juros')
    def valores_devem_ser_positivos(cls, v):
        if v <= 0:
            raise ValueError('Valor deve ser maior que zero')
        return v
    
    @validator('saldo')
    def saldo_maximo(cls, v):
        if v > 10000000:
            raise ValueError('Saldo máximo é R$ 10.000.000,00')
        return v
    
    @validator('parcela')
    def parcela_maxima(cls, v):
        if v > 1000000:
            raise ValueError('Parcela máxima é R$ 1.000.000,00')
        return v
    
    @validator('juros')
    def juros_maximos(cls, v):
        if v > 50:
            raise ValueError('Juros máximos são 50% ao mês')
        return v

class SimulacaoValidator(BaseModel):
    emprestimos: List[EmprestimoValidator]
    aporte_fixo: Decimal
    aporte_extra: Decimal
    
    @validator('aporte_fixo', 'aporte_extra')
    def aportes_devem_ser_positivos(cls, v):
        if v < 0:
            raise ValueError('Aporte não pode ser negativo')
        if v > 1000000:
            raise ValueError('Aporte máximo é R$ 1.000.000,00')
        return v 