from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List

from app.modules.boleto_analysis.domain.value_objects.boleto_amount_vo import (
    BoletoAmount,
)

from app.modules.boleto_analysis.domain.value_objects.boleto_code_vo import (
    BoletoCode,
    BoletoType,
)

from app.modules.boleto_analysis.domain.value_objects.due_date_vo import (
    DueDate,
)


@dataclass(frozen=True)
class BoletoValidationEntity:
    """
    Entidade de domínio que representa a validação de um boleto.
    """

    user_id: str

    code: BoletoCode
    amount: BoletoAmount
    due_date: DueDate

    status: str
    reasons: List[str]

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    # ------------------------------------------------------------------
    # Fábrica de domínio
    # ------------------------------------------------------------------

    @staticmethod
    def validate(
        code: BoletoCode,
        user_id: str,
    ) -> "BoletoValidationEntity":
        """
        Executa todas as regras de validação sobre o código já construído.
        """

        reasons: List[str] = []
        status = "valid"

        # Extrai amount e due_date a partir do código
        amount = BoletoValidationEntity._extract_amount(code)
        due_date = BoletoValidationEntity._extract_due_date(code)

        # Regra 1: vencimento
        if due_date.is_expired:
            reasons.append(
                f"Boleto vencido há {due_date.days_overdue} dia(s) "
                f"(vencimento: {due_date})."
            )
            status = "expired"

        # Regra 2: valor zerado
        if amount.is_zero:
            reasons.append(
                "Boleto sem valor fixo — confirme o valor antes de pagar."
            )

            if status == "valid":
                status = "suspicious"

        # Regra 3: valor suspeito (alto)
        if amount.is_suspicious:
            reasons.append(
                f"Valor elevado detectado ({amount}) — verifique antes de pagar."
            )

            if status == "valid":
                status = "suspicious"

        return BoletoValidationEntity(
            user_id=user_id,
            code=code,
            amount=amount,
            due_date=due_date,
            status=status,
            reasons=reasons,
        )

    # ------------------------------------------------------------------
    # Helpers privados de extração
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_amount(code: BoletoCode) -> BoletoAmount:
        return BoletoAmount.from_raw_digits(code.raw_amount)

    @staticmethod
    def _extract_due_date(code: BoletoCode) -> DueDate:
        if (
            code.boleto_type == BoletoType.COBRANCA
            and code.due_date_factor
        ):
            return DueDate.from_factor(code.due_date_factor)

        return DueDate.no_due_date()
