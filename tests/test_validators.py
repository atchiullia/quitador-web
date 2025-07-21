import pytest
from app.application.validators import EmprestimoValidator, SimulacaoValidator
from decimal import Decimal

class TestEmprestimoValidator:
    def test_nome_valido(self):
        data = {
            'nome': 'Empréstimo Teste',
            'saldo': Decimal('10000'),
            'parcela': Decimal('500'),
            'juros': Decimal('2.5')
        }
        validator = EmprestimoValidator(**data)
        assert validator.nome == 'Empréstimo Teste'
    
    def test_nome_vazio(self):
        data = {
            'nome': '',
            'saldo': Decimal('10000'),
            'parcela': Decimal('500'),
            'juros': Decimal('2.5')
        }
        with pytest.raises(ValueError, match='Nome é obrigatório'):
            EmprestimoValidator(**data)
    
    def test_saldo_maximo_excedido(self):
        data = {
            'nome': 'Empréstimo Teste',
            'saldo': Decimal('15000000'),
            'parcela': Decimal('500'),
            'juros': Decimal('2.5')
        }
        with pytest.raises(ValueError, match='Saldo máximo'):
            EmprestimoValidator(**data) 