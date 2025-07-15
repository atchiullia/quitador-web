from flask import Blueprint, render_template, request, send_file, flash, redirect, url_for
from io import BytesIO
from .simulator import Emprestimo, simular_quitacao_snowball

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Ler aportes
        try:
            aporte_fixo = float(request.form.get("aporte_fixo", "0").replace(",", "."))
        except ValueError:
            aporte_fixo = 0.0

        try:
            aporte_extra = float(request.form.get("aporte_extra", "0").replace(",", "."))
        except ValueError:
            aporte_extra = 0.0

        # Ler empréstimos dinâmicos
        nomes = request.form.getlist("nome[]")
        saldos = request.form.getlist("saldo[]")
        parcelas = request.form.getlist("parcela[]")
        juros = request.form.getlist("juros[]")

        emprestimos = []
        for n, s, p, j in zip(nomes, saldos, parcelas, juros):
            try:
                saldo = float(s.replace(",", "."))
                parcela = float(p.replace(",", "."))
                juros_mensal = float(j.replace(",", "."))
                if saldo > 0 and parcela > 0 and juros_mensal >= 0 and n.strip() != "":
                    emprestimos.append(Emprestimo(n.strip(), saldo, parcela, juros_mensal))
            except ValueError:
                continue  # Ignorar entradas inválidas

        if not emprestimos:
            flash("Por favor, informe ao menos um empréstimo válido.", "error")
            return redirect(url_for("main.index"))

        df = simular_quitacao_snowball(emprestimos, aporte_fixo, aporte_extra)

        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)
        return send_file(
            output,
            as_attachment=True,
            download_name="simulacao_quitacao_snowball.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    return render_template("index.html")
