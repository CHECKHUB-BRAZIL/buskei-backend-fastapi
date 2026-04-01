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
    def analyze(url: URL) -> "LinkAnalysisEntity":
        """
        Executa a análise de segurança do link.

        Regras:
        - HTTP → risco alto
        - Domínio inválido → risco alto
        - Palavras suspeitas → risco médio
        """

        reasons: List[str] = []
        risk = "safe"

        # regra 1: HTTPS
        if not url.is_https:
            reasons.append("Não usa HTTPS")
            risk = "high"

        # regra 2: domínio inválido
        if "." not in url.domain:
            reasons.append("Domínio inválido")
            risk = "high"

        # regra 3: palavras suspeitas
        if url.has_suspicious_words:
            reasons.append("URL contém palavras suspeitas")
            if risk != "high":
                risk = "medium"

        return LinkAnalysisEntity(
            url=url,
            risk=risk,
            reasons=reasons,
        )
