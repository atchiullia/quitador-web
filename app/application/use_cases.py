
from io import BytesIO
from app.application.exceptions import SimulacaoBusinessError, SimulacaoValidationError
from app.domain.models import Emprestimo
from app.domain.services import simular_quitacao_snowball
from app.application.dto import SimulacaoRequestDTO, SimulacaoResponseDTO, EmprestimoDTO

import logging

logger = logging.getLogger(__name__)

def simular_quitacao_use_case(
    nomes, saldos, parcelas, juros, aporte_fixo, aporte_extra, meses_maximos=120
) -> SimulacaoResponseDTO:
    logger.info("Iniciando simulação de quitação.")
    # Validação e parsing dos dados
    emprestimos = []
    for n, s, p, j in zip(nomes, saldos, parcelas, juros):
        try:
            saldo = float(s.replace(",", "."))
            parcela = float(p.replace(",", "."))
            juros_mensal = float(j.replace(",", "."))
            if saldo > 0 and parcela > 0 and juros_mensal >= 0 and n.strip() != "":
                logger.debug(f"Adicionando empréstimo válido: {n.strip()}")
                emprestimos.append(Emprestimo(
                    nome=n.strip(),
                    saldo=saldo,
                    parcela=parcela,
                    juros_mensal=juros_mensal,
                    entra_no_aporte=True  # ou conforme sua lógica
                ))
            else:
                logger.warning(f"Empréstimo ignorado: dados inválidos - nome={n}, saldo={s}, parcela={p}, juros={j}")
        except ValueError as e:
            logger.error(f"Erro ao converter valores do empréstimo: {e}")
            continue

    if not emprestimos:
        logger.error("Nenhum empréstimo válido informado.")
        raise SimulacaoValidationError("Nenhum empréstimo válido informado.")

    logger.info(f"Total de empréstimos válidos: {len(emprestimos)}")
    try:
        df = simular_quitacao_snowball(emprestimos, aporte_fixo, aporte_extra)
    except Exception as e:
        logger.exception("Erro durante a simulação de quitação.")
        raise SimulacaoBusinessError(f"Erro durante a simulação de quitação. {str(e)}")
    else:
        if len(df) >= 120:
            logger.warning("Simulação excedeu 120 meses.")
            raise SimulacaoBusinessError(f"A simulação excedeu o limite de 120 meses. Ajuste os valores para quitar mais rápido.")
        try:
            output = BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)
            logger.info("Simulação e geração de planilha concluídas com sucesso.")
            return SimulacaoResponseDTO(resultado=df.to_dict(orient="records"))
        except Exception as e:
            logger.exception("Erro ao gerar ou enviar o arquivo Excel.")
            raise SimulacaoBusinessError(f"Erro ao gerar planilha do Excel: {str(e)}")
        
    finally:
        logger.info("Processamento da requisição POST finalizado.")

