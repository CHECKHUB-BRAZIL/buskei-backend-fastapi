import re
import tldextract


class LinkAnalysisService:

    def analyze(self, url: str) -> tuple[int, list[str]]:
        reasons = []
        risk_score = 0

        ext = tldextract.extract(url)

        # evita domínio vazio tipo "http://..."
        if not ext.domain or not ext.suffix:
            reasons.append("Domínio inválido")
            risk_score += 50

        # HTTPS
        if not url.startswith("https://"):
            reasons.append("Site não usa HTTPS")
            risk_score += 30

        # IP
        if re.match(r"http[s]?://\d+\.\d+\.\d+\.\d+", url):
            reasons.append("URL usa IP em vez de domínio")
            risk_score += 40

        # tamanho
        if len(url) > 100:
            reasons.append("URL muito longa")
            risk_score += 10

        # phishing keywords
        suspicious_words = ["login", "verify", "update", "bank", "secure"]
        if any(word in url.lower() for word in suspicious_words):
            reasons.append("Possível tentativa de phishing")
            risk_score += 20

        # subdomínios
        if url.count('.') > 3:
            reasons.append("Muitos subdomínios")
            risk_score += 15

        # TLD suspeito
        suspicious_tlds = ["xyz", "top", "click", "loan"]
        if ext.suffix in suspicious_tlds:
            reasons.append("TLD suspeito")
            risk_score += 25

        return risk_score, reasons
