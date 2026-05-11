from app.modules.boleto_analysis.domain.risk.boleto_risk_signal import (
    BoletoRiskSignal,
)

from app.modules.boleto_analysis.domain.value_objects.boleto_code_vo import (
    BoletoCode,
    BoletoType,
)


class BoletoAnalysisService:
    """
    Serviço de análise heurística antifraude.

    Responsável por detectar sinais de risco em boletos.
    """

    def analyze(
        self,
        code: BoletoCode,
    ) -> list[BoletoRiskSignal]:

        signals: list[BoletoRiskSignal] = []

        # ======================================================
        # DV inválido
        # ======================================================

        if not code.is_real:
            signals.append(
                BoletoRiskSignal(
                    code="INVALID_CHECK_DIGIT",
                    message=(
                        "O dígito verificador é inválido. "
                        "Pode indicar boleto falso ou erro de digitação."
                    ),
                    score=60,
                )
            )

        # ======================================================
        # Banco não identificado
        # ======================================================

        if (
            code.boleto_type == BoletoType.COBRANCA
            and not code.bank_code
        ):
            signals.append(
                BoletoRiskSignal(
                    code="UNKNOWN_BANK",
                    message="Não foi possível identificar o banco emissor.",
                    score=20,
                )
            )

        # ======================================================
        # Boleto sem valor
        # ======================================================

        raw = code.raw_amount

        if raw == ("0" * len(raw)):
            signals.append(
                BoletoRiskSignal(
                    code="ZERO_AMOUNT",
                    message=(
                        "Boleto sem valor definido. "
                        "Recomenda-se validação manual."
                    ),
                    score=25,
                )
            )

        # ======================================================
        # Estrutura fora do padrão
        # ======================================================

        if len(code.value) != 44:
            signals.append(
                BoletoRiskSignal(
                    code="INVALID_STRUCTURE",
                    message=(
                        "Estrutura do código fora do padrão Febraban."
                    ),
                    score=40,
                )
            )

        return signals
