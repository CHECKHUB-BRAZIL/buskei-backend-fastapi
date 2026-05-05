from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

from app.modules.boleto_analysis.domain.exceptions.exceptions import InvalidAmountError


@dataclass(frozen=True)
class BoletoAmount:
    """
    Value Object que representa o valor monetário de um boleto.

    Características:
    - Usa Decimal para evitar erros de ponto flutuante.
    - Nunca negativo.
    - Precisão de 2 casas decimais.
    - Valor zero é permitido (boleto sem valor fixo).
    """

    value: Decimal

    def __post_init__(self) -> None:

        try:
            normalized = Decimal(str(self.value)).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
        except (InvalidOperation, ValueError):
            raise InvalidAmountError(str(self.value))

        if normalized < Decimal("0"):
            raise InvalidAmountError(str(self.value), "Valor não pode ser negativo.")

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return f"R$ {self.value:,.2f}"

    # ------------------------------------------------------------------
    # Fábrica a partir do código de barras (10 dígitos brutos)
    # ------------------------------------------------------------------

    @classmethod
    def from_raw_digits(cls, raw: str) -> "BoletoAmount":
        """
        Converte os 10 dígitos de valor extraídos do código de barras
        para um BoletoAmount.

        Os dois últimos dígitos representam centavos.
        Ex: '0000012500' → R$ 125,00
        """
        if not raw.isdigit() or len(raw) != 10:
            raise InvalidAmountError(raw, "Sequência de valor inválida no código de barras.")

        reais = int(raw[:-2])
        centavos = int(raw[-2:])
        total = Decimal(reais) + Decimal(centavos) / Decimal("100")
        return cls(value=total)

    # ------------------------------------------------------------------
    # Propriedades de domínio
    # ------------------------------------------------------------------

    @property
    def is_zero(self) -> bool:
        """Boleto sem valor fixo (valor em aberto definido pelo pagador)."""
        return self.value == Decimal("0")

    @property
    def is_suspicious(self) -> bool:
        """
        Valor acima de R$ 50.000,00 é marcado como suspeito para revisão manual.
        Threshold configurável conforme regra de negócio.
        """
        SUSPICIOUS_THRESHOLD = Decimal("50000.00")
        return self.value > SUSPICIOUS_THRESHOLD
