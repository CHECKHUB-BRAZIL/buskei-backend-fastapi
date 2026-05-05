from dataclasses import dataclass
from datetime import date, timedelta


# Data base Febraban: fator 1000 = 03/07/2000
_FEBRABAN_BASE_DATE = date(2000, 7, 3)
_FEBRABAN_FACTOR_BASE = 1000

# Fator máximo antes do ciclo (reinicia em 1000 após atingir 9999)
_FACTOR_MAX = 9999
_FACTOR_CYCLE_RESET = 1000


@dataclass(frozen=True)
class DueDate:
    """
    Value Object que representa a data de vencimento de um boleto.

    Características:
    - Calculada a partir do fator de vencimento Febraban (4 dígitos).
    - Fator '0000' indica boleto sem data de vencimento.
    - Expõe se o boleto está vencido e por quantos dias.
    """

    value: date | None  # None = sem vencimento definido
    factor: str         # fator original do código de barras (4 dígitos)

    def __str__(self) -> str:
        if self.value is None:
            return "Sem vencimento"
        return self.value.strftime("%d/%m/%Y")

    # ------------------------------------------------------------------
    # Fábrica
    # ------------------------------------------------------------------

    @classmethod
    def from_factor(cls, factor: str) -> "DueDate":
        """
        Converte o fator de vencimento Febraban (4 dígitos) em DueDate.

        Fator '0000': sem vencimento.
        Demais valores: data = BASE + (fator - BASE_FACTOR) dias,
        com tratamento do ciclo de reinício após 9999.
        """
        if not factor.isdigit() or len(factor) != 4:
            raise ValueError(f"Fator de vencimento inválido: '{factor}'")

        int_factor = int(factor)

        if int_factor == 0:
            return cls(value=None, factor=factor)

        # Tratamento do ciclo: após 9999 o fator volta a 1000
        delta = int_factor - _FEBRABAN_FACTOR_BASE
        if delta < 0:
            # Ocorreu o ciclo de reinício
            delta += (_FACTOR_MAX - _FEBRABAN_FACTOR_BASE + 1)

        due = _FEBRABAN_BASE_DATE + timedelta(days=delta)
        return cls(value=due, factor=factor)

    @classmethod
    def no_due_date(cls) -> "DueDate":
        """Convênio: sem data de vencimento."""
        return cls(value=None, factor="0000")

    # ------------------------------------------------------------------
    # Propriedades de domínio
    # ------------------------------------------------------------------

    @property
    def has_due_date(self) -> bool:
        return self.value is not None

    @property
    def is_expired(self) -> bool:
        """Boleto vencido em relação à data atual."""
        if self.value is None:
            return False
        return self.value < date.today()

    @property
    def days_overdue(self) -> int:
        """Quantos dias de atraso. Retorna 0 se não vencido ou sem data."""
        if not self.is_expired:
            return 0
        return (date.today() - self.value).days

    @property
    def days_until_due(self) -> int | None:
        """Dias restantes até o vencimento. None se sem data ou já vencido."""
        if self.value is None or self.is_expired:
            return None
        return (self.value - date.today()).days
