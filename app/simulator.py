import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .models import Emprestimo

def simular_quitacao_snowball(
    emprestimos,
    aporte_fixo,
    aporte_extra=0.0,
    inicio=datetime(2025, 8, 1),
    meses_maximos=120
):
    resultado = []
    extra_aporte = aporte_fixo
    emprestimos_ativos = emprestimos.copy()

    for i in range(meses_maximos):
        data_atual = inicio + relativedelta(months=i)
        linha = {"Mês": data_atual.strftime("%b %Y")}
        total_pago = 0
        notas = ""

        for emp in emprestimos_ativos:
            if emp.pago:
                linha[emp.nome] = 0
                continue

            juros = emp.saldo * emp.juros_mensal
            pagamento = emp.parcela

            if emp == next(e for e in emprestimos_ativos if not e.pago):
                pagamento += extra_aporte + aporte_extra

            amortizacao = pagamento - juros
            if amortizacao > emp.saldo:
                amortizacao = emp.saldo
                pagamento = juros + amortizacao

            emp.saldo -= amortizacao
            linha[emp.nome] = round(pagamento, 2)
            total_pago += pagamento

            if emp.saldo <= 0.01:
                emp.pago = True
                if emp.entra_no_aporte:
                    extra_aporte += emp.parcela
                notas += f"{emp.nome} quitado. "

        linha["Aporte Fixo"] = round(extra_aporte, 2)
        linha["Aporte Extra"] = round(aporte_extra, 2)
        linha["Total Pago"] = round(total_pago, 2)
        linha["Notas"] = notas.strip()
        resultado.append(linha)

        if all(emp.pago for emp in emprestimos_ativos):
            break

    return pd.DataFrame(resultado)
