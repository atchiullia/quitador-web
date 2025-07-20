# app/application/exceptions.py

class SimulacaoValidationError(Exception):
    """Erro de validação nos dados da simulação."""
    pass

class SimulacaoBusinessError(Exception):
    """Erro de regra de negócio na simulação."""
    pass
