from dataclasses import dataclass
from urllib.parse import urlparse

from app.modules.link_analysis.domain.exceptions.exceptions import (
    InvalidURLError,
    UnsupportedSchemeError,
    URLTooLongError,
)


@dataclass(frozen=True)
class URLVO:
    """
    Value Object que representa uma URL válida.
    """

    value: str

    MAX_LENGTH = 2083

    def __post_init__(self):

        normalized = self.value.strip().lower()

        object.__setattr__(self, "value", normalized)

        # ------------------------------------------------------
        # tamanho
        # ------------------------------------------------------

        if len(normalized) > self.MAX_LENGTH:
            raise URLTooLongError(normalized)

        # ------------------------------------------------------
        # parsing
        # ------------------------------------------------------

        parsed = urlparse(normalized)

        if not parsed.scheme or not parsed.netloc:
            raise InvalidURLError(normalized)

        # ------------------------------------------------------
        # schemes suportados
        # ------------------------------------------------------

        if parsed.scheme not in ("http", "https"):
            raise UnsupportedSchemeError(parsed.scheme)

        # cache interno
        object.__setattr__(self, "_parsed", parsed)

    def __str__(self) -> str:
        return self.value

    # ==========================================================
    # PROPERTIES
    # ==========================================================

    @property
    def scheme(self) -> str:
        return self._parsed.scheme

    @property
    def domain(self) -> str:
        return self._parsed.netloc

    @property
    def path(self) -> str:
        return self._parsed.path

    @property
    def is_https(self) -> bool:
        return self.scheme == "https"

    @property
    def has_suspicious_words(self) -> bool:
        suspicious_words = [
            "login",
            "verify",
            "bank",
            "update",
            "secure",
        ]

        return any(
            word in self.value
            for word in suspicious_words
        )

    @property
    def subdomain_count(self) -> int:
        return self.domain.count(".")
