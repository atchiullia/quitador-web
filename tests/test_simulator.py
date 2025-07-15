import pytest
import pandas as pd
from datetime import datetime
from app.simulator import simular_quitacao_snowball
from app.models import Emprestimo


def criar_emprestimos_basicos():
    return [
        Emprestimo("Empréstimo A", 1000, 200, 2.0),
        Emprestimo("Empréstimo B", 500, 100, 1.5)
    ]


def test_simulacao_gera_dataframe():
    emprestimos = criar_emprestimos_basicos()
    df = simular_quitacao_snowball(emprestimos, aporte_fixo=100)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_quitacao_completa():
    emprestimos = criar_emprestimos_basicos()
    df = simular_quitacao_snowball(emprestimos, aporte_fixo=100)

    # Última linha deve conter todos quitados
    ultima_linha = df.iloc[-1]
    assert "Empréstimo A quitado." in ultima_linha["Notas"]
    assert "Empréstimo B quitado." in ultima_linha["Notas"]


def test_aporte_extra_influencia_total_pago():
    emprestimos1 = criar_emprestimos_basicos()
    emprestimos2 = criar_emprestimos_basicos()

    df_sem_extra = simular_quitacao_snowball(emprestimos1, aporte_fixo=100, aporte_extra=0)
    df_com_extra = simular_quitacao_snowball(emprestimos2, aporte_fixo=100, aporte_extra=300)

    assert df_com_extra["Total Pago"].sum() < df_sem_extra["Total Pago"].sum()


def test_emprestimo_sem_aporte_nao_aumenta_extra_aporte():
    emprestimos = [
        Emprestimo("A", 1000, 200, 2.0, entra_no_aporte=False),
        Emprestimo("B", 1000, 200, 2.0)
    ]
    df = simular_quitacao_snowball(emprestimos, aporte_fixo=100)
    
    for linha in df["Aporte Fixo"]:
        assert linha <= 500  # nunca deve ultrapassar 100 (inicial) + 200 (de B)


def test_limite_meses_maximos_respeitado():
    emprestimos = [
        Emprestimo("Lento", 100000, 100, 1.0)
    ]
    df = simular_quitacao_snowball(emprestimos, aporte_fixo=0, meses_maximos=12)
    assert len(df) == 12 or emprestimos[0].pago
