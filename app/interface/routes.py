from app.application.exceptions import SimulacaoBusinessError, SimulacaoValidationError
from flask import Blueprint, render_template, request, send_file, flash, redirect, url_for, current_app, jsonify
from io import BytesIO
from app.application.dto import EmprestimoDTO, SimulacaoRequestDTO, SimulacaoSnowballRequest
from app.domain.services import simular_quitacao_snowball
from app.domain.models import Emprestimo
from app.application.use_cases import simular_quitacao_use_case
import pandas as pd

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Criar DTO e validar
            simulacao_request = SimulacaoSnowballRequest.from_form_data(request.form)
            errors = simulacao_request.validate()
            
            if errors:
                return jsonify({
                    'success': False,
                    'errors': errors
                }), 400
            
            # Processar simulação usando use case existente
            response_dto = simular_quitacao_use_case(
                simulacao_request.nomes,
                simulacao_request.saldos,
                simulacao_request.parcelas,
                simulacao_request.juros,
                simulacao_request.aporte_fixo,
                simulacao_request.aporte_extra
            )
            
            # Retornar arquivo Excel
            df = pd.DataFrame(response_dto.resultado)
            output = BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)
            
            return send_file(
                output,
                as_attachment=True,
                download_name='simulacao_snowball.xlsx',
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
        except SimulacaoValidationError as ve:
            return jsonify({
                'success': False,
                'errors': [str(ve)]
            }), 400
            
        except SimulacaoBusinessError as be:
            return jsonify({
                'success': False,
                'errors': [str(be)]
            }), 400
            
        except Exception as e:
            current_app.logger.exception("Erro inesperado na simulação.")
            return jsonify({
                'success': False,
                'errors': [f"Erro interno: {str(e)}"]
            }), 500
    
    return render_template('index.html')
