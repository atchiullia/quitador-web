from app.application.exceptions import SimulacaoBusinessError, SimulacaoValidationError
from flask import Blueprint, render_template, request, send_file, flash, redirect, url_for, current_app
from io import BytesIO
from app.application.dto import EmprestimoDTO, SimulacaoRequestDTO
from app.domain.services import simular_quitacao_snowball
from app.domain.models import Emprestimo
from app.application.use_cases import simular_quitacao_use_case
import pandas as pd

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            nomes = request.form.getlist("nome[]")
            saldos = request.form.getlist("saldo[]")
            parcelas = request.form.getlist("parcela[]")
            juros = request.form.getlist("juros[]")
            aporte_fixo = request.form.get("aporte_fixo", "0")
            aporte_extra = request.form.get("aporte_extra", "0")

            response_dto = simular_quitacao_use_case(
                    nomes, saldos, parcelas, juros, aporte_fixo, aporte_extra
                )
            df = pd.DataFrame(response_dto.resultado)
            output = BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)
            return send_file(
                    output,
                    as_attachment=True,
                    download_name="simulacao_quitacao_snowball.xlsx",
                    mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except SimulacaoValidationError as ve:
            flash(str(ve), "error")
            return redirect(url_for("main.index"))
        except SimulacaoBusinessError as be:
            flash(str(be), "error")
            return redirect(url_for("main.index"))
        except Exception as e:
            current_app.logger.exception("Erro inesperado na simulação.")
            flash("Erro interno na simulação.", "error")
            return redirect(url_for("main.index"))

    return render_template("index.html")
