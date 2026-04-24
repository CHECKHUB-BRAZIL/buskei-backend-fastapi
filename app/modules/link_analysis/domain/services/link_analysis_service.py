import re
import tldextract
class LinkAnalysisService:

    def analyze(self, url: str) -> tuple[int, list[str]]:
        reasons = []
        positives = []
        risk_score = 0

        ext = tldextract.extract(url)

        # Domínio válido
        if not ext.domain or not ext.suffix:
            reasons.append("O link não possui um domínio válido, o que pode indicar um site malformado ou suspeito.")
            risk_score += 50
        else:
            positives.append(f"O domínio '{ext.domain}.{ext.suffix}' parece válido.")

        # HTTPS
        if not url.startswith("https://"):
            reasons.append("O site não utiliza HTTPS, o que significa que a conexão pode não ser segura.")
            risk_score += 30
        else:
            positives.append("O site utiliza HTTPS, indicando uma conexão segura.")

        # IP
        if re.match(r"http[s]?://\d+\.\d+\.\d+\.\d+", url):
            reasons.append("O link utiliza um endereço IP em vez de um domínio, o que é comum em links maliciosos.")
            risk_score += 40
        else:
            positives.append("O link utiliza um domínio em vez de um endereço IP, o que é mais confiável.")

        # tamanho
        if len(url) > 100:
            reasons.append("O link é muito longo, o que pode ser usado para esconder partes suspeitas.")
            risk_score += 10
        else:
            positives.append("O tamanho do link está dentro do padrão esperado.")

        # phishing keywords
        suspicious_words = ["login", "verify", "update", "bank", "secure"]
        if any(word in url.lower() for word in suspicious_words):
            reasons.append("O link contém palavras comuns em golpes de phishing, como 'login' ou 'verify'.")
            risk_score += 20
        else:
            positives.append("Não foram identificadas palavras suspeitas no link.")

        # subdomínios
        if url.count('.') > 3:
            reasons.append("O link possui muitos subdomínios, o que pode ser uma tentativa de enganar o usuário.")
            risk_score += 15
        else:
            positives.append("A estrutura do domínio parece normal, sem excesso de subdomínios.")

        # TLD suspeito
        suspicious_tlds = ["xyz", "top", "click", "loan"]

        if not ext.suffix:
            reasons.append("O link não possui um domínio válido com TLD, o que é altamente suspeito.")
            risk_score += 40

        elif ext.suffix in suspicious_tlds:
            reasons.append(f"O domínio utiliza um TLD suspeito (.{ext.suffix}), frequentemente associado a golpes.")
            risk_score += 25

        else:
            positives.append(f"O domínio utiliza um TLD comum e confiável (.{ext.suffix}).")

        # Caso totalmente seguro
        if not reasons:
            positives.insert(0, "Nenhum problema foi identificado neste link.")
            return risk_score, positives

        # Mistura feedback negativo + positivo
        return risk_score, reasons + positives
