import re
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class URL:
    """
    Value Object que representa uma URL válida.

    Características:
    - Imutável
    - Normaliza valor
    - Valida formato básico
    """

    value: str

    def __post_init__(self):
        # Normaliza
        normalized = self.value.strip().lower()
        object.__setattr__(self, "value", normalized)

        parsed = urlparse(normalized)

        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"URL inválida: {self.value}")

    def __str__(self) -> str:
        return self.value

    # -------------------------
    # Propriedades de domínio
    # -------------------------

    @property
    def is_https(self) -> bool:
        return self.value.startswith("https")

    @property
    def domain(self) -> str:
        return urlparse(self.value).netloc

    @property
    def has_suspicious_words(self) -> bool:
        suspicious_words = ["login", "verify", "bank", "update"]
        return any(word in self.value for word in suspicious_words)
