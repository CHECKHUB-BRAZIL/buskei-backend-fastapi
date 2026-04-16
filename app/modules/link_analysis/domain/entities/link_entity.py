from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List

from app.modules.link_analysis.domain.value_objects.url_vo import URL


@dataclass(frozen=True)
class LinkAnalysisEntity:
    """
    Entidade de domínio que representa a análise de segurança de um link.

    Princípios:
    - Imutável
    - Regras de domínio encapsuladas
    - Não depende de infraestrutura
    """

    url: URL
    risk: str
    reasons: List[str]
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    # ------------------------------------------------------------------
    # Fábrica de domínio (factory)
    # ------------------------------------------------------------------

    @staticmethod
    def create(
        url: URL,
        risk: str,
        reasons: List[str],
    ) -> "LinkAnalysisEntity":
        return LinkAnalysisEntity(
            url=url,
            risk=risk,
            reasons=reasons,
        )
