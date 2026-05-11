from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
import re

from app.modules.boleto_analysis.domain.exceptions.exceptions import InvalidAmountError


@dataclass(frozen=True)
class BoletoAmount:
    """
    Value Object que representa o valor monetário de um boleto.

    Responsabilidades:
    - Garantir formato válido
    - Garantir precisão decimal
    - Evitar valores negativos
    """

    value: Decimal

    def __post_init__(self) -> None:

        try:
            normalized = Decimal(str(self.value)).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        except (InvalidOperation, ValueError):
            raise InvalidAmountError(str(self.value))

        if normalized < Decimal("0"):
            raise InvalidAmountError(
                str(self.value),
                "Valor não pode ser negativo.",
            )

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return f"R$ {self.value:,.2f}"

    # ----------------------------------------------------------
    # FACTORY
    # ----------------------------------------------------------

    @classmethod
    def from_raw_digits(cls, raw: str) -> "BoletoAmount":
        """
        Converte os 10 dígitos de valor do código de barras
        em um valor monetário.
        """

        raw = re.sub(r"\D", "", raw.strip())

        if len(raw) != 10:
            raise InvalidAmountError(
                raw,
                "Sequência de valor inválida no código de barras.",
            )

        reais = int(raw[:-2])
        centavos = int(raw[-2:])

        total = Decimal(reais) + (Decimal(centavos) / Decimal("100"))

        return cls(value=total)

    # ----------------------------------------------------------
    # PROPERTIES
    # ----------------------------------------------------------

    @property
    def is_zero(self) -> bool:
        """
        Indica boleto sem valor definido (valor zero).
        """
        return self.value == Decimal("0.00")

    @property
    def is_suspicious(self) -> bool:
        """
        Valor acima de um limite configurado pode indicar risco.
        """
        SUSPICIOUS_THRESHOLD = Decimal("50000.00")
        return self.value > SUSPICIOUS_THRESHOLD
