import re

import tldextract

from app.modules.link_analysis.domain.value_objects.url_vo import (
    URL,
)


class LinkAnalysisService:
    """
    Serviço de análise heurística antifraude de links.
    """

    SUSPICIOUS_TLDS = {
        "xyz",
        "top",
        "click",
        "loan",
    }

    def analyze(
        self,
        url: URL,
    ) -> tuple[int, list[str], list[str]]:
        """
        Retorna:
            - risk_score
            - reasons
            - positives
        """

        reasons: list[str] = []
        positives: list[str] = []

        risk_score = 0

        ext = tldextract.extract(url.value)

        # ======================================================
        # HTTPS
        # ======================================================

        if not url.is_https:
            reasons.append(
                "O site não utiliza HTTPS, o que significa que a conexão pode não ser segura."
            )

            risk_score += 30

        else:
            positives.append(
                "O site utiliza HTTPS, indicando uma conexão segura."
            )

        # ======================================================
        # DOMÍNIO
        # ======================================================

        if ext.domain and ext.suffix:
            positives.append(
                f"O domínio '{ext.domain}.{ext.suffix}' parece válido."
            )

        else:
            reasons.append(
                "O link não possui um domínio válido."
            )

            risk_score += 50

        # ======================================================
        # IP ADDRESS
        # ======================================================

        if re.match(
            r"http[s]?://\d+\.\d+\.\d+\.\d+",
            url.value,
        ):
            reasons.append(
                "O link utiliza um endereço IP em vez de domínio, comportamento comum em links maliciosos."
            )

            risk_score += 40

        else:
            positives.append(
                "O link utiliza domínio em vez de endereço IP."
            )

        # ======================================================
        # TAMANHO
        # ======================================================

        if len(url.value) > 100:
            reasons.append(
                "O link é muito longo, o que pode ocultar partes suspeitas."
            )

            risk_score += 10

        else:
            positives.append(
                "O tamanho do link está dentro do esperado."
            )

        # ======================================================
        # PALAVRAS SUSPEITAS
        # ======================================================

        if url.has_suspicious_words:
            reasons.append(
                "O link contém palavras frequentemente usadas em golpes de phishing."
            )

            risk_score += 20

        else:
            positives.append(
                "Não foram identificadas palavras suspeitas."
            )

        # ======================================================
        # SUBDOMÍNIOS
        # ======================================================

        if url.subdomain_count > 3:
            reasons.append(
                "O link possui muitos subdomínios, o que pode indicar tentativa de enganar o usuário."
            )

            risk_score += 15

        else:
            positives.append(
                "A estrutura do domínio parece normal."
            )

        # ======================================================
        # TLD SUSPEITO
        # ======================================================

        if ext.suffix in self.SUSPICIOUS_TLDS:

            reasons.append(
                f"O domínio utiliza um TLD suspeito (.{ext.suffix})."
            )

            risk_score += 25

        else:
            positives.append(
                f"O domínio utiliza um TLD comum (.{ext.suffix})."
            )

        # ======================================================
        # RESULTADO FINAL
        # ======================================================

        if not reasons:

            positives.insert(
                0,
                "Nenhum problema foi identificado neste link.",
            )

        return risk_score, reasons, positives
