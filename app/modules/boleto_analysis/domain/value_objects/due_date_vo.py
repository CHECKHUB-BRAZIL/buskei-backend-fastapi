from dataclasses import dataclass
from datetime import date, timedelta


_FEBRABAN_BASE_DATE = date(2000, 7, 3)
_FEBRABAN_FACTOR_BASE = 1000
_FACTOR_MAX = 9999


@dataclass(frozen=True)
class DueDate:
    """
    Value Object de vencimento do boleto.

    Responsabilidades:
    - Converter fator Febraban em data
    - Permitir análise externa (antifraude)
    - NÃO depende de date.today() internamente
    """

    value: date | None
    factor: str

    def __str__(self) -> str:
        if self.value is None:
            return "Sem vencimento"
        return self.value.strftime("%d/%m/%Y")

    # ----------------------------------------------------------
    # FACTORY
    # ----------------------------------------------------------

    @classmethod
    def from_factor(cls, factor: str) -> "DueDate":

        if not factor.isdigit() or len(factor) != 4:
            raise ValueError(f"Fator de vencimento inválido: '{factor}'")

        int_factor = int(factor)

        if int_factor == 0:
            return cls(value=None, factor=factor)

        delta = int_factor - _FEBRABAN_FACTOR_BASE

        if delta < 0:
            delta += (_FACTOR_MAX - _FEBRABAN_FACTOR_BASE + 1)

        due = _FEBRABAN_BASE_DATE + timedelta(days=delta)

        return cls(value=due, factor=factor)

    @classmethod
    def no_due_date(cls) -> "DueDate":
        return cls(value=None, factor="0000")

    # ----------------------------------------------------------
    # DOMAIN METHODS (compatível com Entity novo)
    # ----------------------------------------------------------

    def is_expired(self, today: date) -> bool:
        if self.value is None:
            return False
        return self.value < today

    def is_due_today(self, today: date) -> bool:
        if self.value is None:
            return False
        return self.value == today

    def days_overdue(self, today: date) -> int:
        if self.value is None or self.value >= today:
            return 0
        return (today - self.value).days

    def days_until_due(self, today: date) -> int | None:
        if self.value is None or self.value < today:
            return None
        return (self.value - today).days

    # ----------------------------------------------------------
    # SIMPLE PROPS (mantido só como conveniência)
    # ----------------------------------------------------------

    @property
    def has_due_date(self) -> bool:
        return self.value is not None
