from datetime import date

from app.modules.boleto_analysis.application.dtos.boleto_validation_dto import (
    ValidateBoletoInputDTO,
    ValidateBoletoOutputDTO,
)

from app.modules.boleto_analysis.application.exceptions.application_exceptions import (
    map_domain_exception,
)

from app.modules.boleto_analysis.domain.exceptions.exceptions import (
    BoletoDomainError,
)

from app.modules.boleto_analysis.domain.services.boleto_analysis_service import (
    BoletoAnalysisService,
)

from app.modules.boleto_analysis.domain.value_objects.boleto_amount_vo import (
    BoletoAmount,
)

from app.modules.boleto_analysis.domain.value_objects.boleto_code_vo import (
    BoletoCode,
)

from app.modules.boleto_analysis.domain.value_objects.due_date_vo import (
    DueDate,
)


class ValidateBoletoUseCase:
    """
    Caso de uso de análise antifraude de boleto.
    """

    def __init__(
        self,
        analysis_service: BoletoAnalysisService,
    ) -> None:
        self._analysis_service = analysis_service

    def execute(
        self,
        input_dto: ValidateBoletoInputDTO,
    ) -> ValidateBoletoOutputDTO:

        # ======================================================
        # Código do boleto
        # ======================================================

        try:
            code = BoletoCode.create(input_dto.code)

        except BoletoDomainError as exc:
            raise map_domain_exception(exc)

        # ======================================================
        # Valor
        # ======================================================

        try:
            amount = BoletoAmount.from_raw_digits(
                code.raw_amount
            )

        except BoletoDomainError as exc:
            raise map_domain_exception(exc)

        # ======================================================
        # Vencimento
        # ======================================================

        try:
            if code.due_date_factor:
                due_date = DueDate.from_factor(
                    code.due_date_factor
                )
            else:
                due_date = DueDate.no_due_date()

        except Exception as exc:
            raise map_domain_exception(exc)

        # ======================================================
        # Risk engine
        # ======================================================

        signals = self._analysis_service.analyze(code)

        risk_score = sum(
            signal.score
            for signal in signals
        )

        reasons = [
            signal.message
            for signal in signals
        ]

        # ======================================================
        # Status antifraude
        # ======================================================

        if risk_score >= 80:
            status = "high_risk"

        elif risk_score >= 40:
            status = "suspicious"

        else:
            status = "safe"

        # ======================================================
        # Output
        # ======================================================

        today = date.today()

        return ValidateBoletoOutputDTO(
            code=str(code),
            original_code=code.original,
            boleto_type=code.boleto_type.value,

            is_real=code.is_real,

            amount=amount.value,
            amount_formatted=str(amount),

            due_date=due_date.value,
            due_date_formatted=str(due_date),

            is_expired=due_date.is_expired(today),
            days_overdue=due_date.days_overdue(today),
            days_until_due=due_date.days_until_due(today),

            risk_score=risk_score,
            status=status,

            reasons=reasons,
        )
