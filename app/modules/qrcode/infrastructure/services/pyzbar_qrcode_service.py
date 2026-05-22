from io import BytesIO
from urllib.parse import urlparse

from PIL import Image
from app.modules.qrcode.domain.exceptions.qrcode_exceptions import InvalidQRCodeException
from app.modules.qrcode.domain.services.qrcode_decoder_service import QRCodeAnalyzerService
from pyzbar.pyzbar import decode


from app.modules.qrcode.domain.value_objects.qrcode_data import (
    QRCodeData,
)


class PyzbarQRCodeService(QRCodeAnalyzerService):
    """
    Implementação concreta do analyzer de QRCode
    utilizando pyzbar.
    """

    SUSPICIOUS_KEYWORDS = [
        "login",
        "seguro",
        "update",
        "verificacao",
        "verify",
        "gift",
        "premio",
        "bonus",
        "pix-premio",
        "pixbonus",
    ]

    TRUSTED_DOMAINS = [
        "gov.br",
        "nubank.com.br",
        "itau.com.br",
        "mercadopago.com.br",
        "picpay.com",
        "paypal.com",
    ]

    def analyze(
        self,
        image_bytes: bytes,
    ) -> QRCodeData:
        """
        Analisa QRCode e executa
        verificações antifraude.
        """

        image = Image.open(
            BytesIO(image_bytes)
        )

        decoded_objects = decode(image)

        if not decoded_objects:
            raise InvalidQRCodeException()

        raw_value = decoded_objects[0].data.decode(
            "utf-8"
        )

        qrcode_type = self._detect_type(
            raw_value
        )

        risk_score = 0

        status = "safe"

        reason = None

        detected_url = None

        is_suspicious_url = False

        has_unknown_domain = False

        # =====================================================
        # URL ANALYSIS
        # =====================================================

        if qrcode_type == "url":
            detected_url = raw_value

            parsed = urlparse(raw_value)

            domain = parsed.netloc.lower()

            has_unknown_domain = not any(
                trusted in domain
                for trusted in self.TRUSTED_DOMAINS
            )

            suspicious_keyword_found = any(
                keyword in raw_value.lower()
                for keyword in self.SUSPICIOUS_KEYWORDS
            )

            if suspicious_keyword_found:
                risk_score += 40

            if has_unknown_domain:
                risk_score += 35

            if raw_value.startswith("http://"):
                risk_score += 15

            is_suspicious_url = (
                risk_score >= 50
            )

        # =====================================================
        # STATUS
        # =====================================================

        if risk_score >= 80:
            status = "fraud_suspect"

            reason = (
                "QRCode com alto risco de fraude."
            )

        elif risk_score >= 50:
            status = "suspicious"

            reason = (
                "QRCode requer atenção."
            )

        else:
            status = "safe"

        return QRCodeData(
            raw_value=raw_value,
            qrcode_type=qrcode_type,
            is_valid=True,
            risk_score=risk_score,
            status=status,
            reason=reason,
            pix_key=None,
            merchant_name=None,
            amount=None,
            detected_url=detected_url,
            is_suspicious_url=is_suspicious_url,
            has_unknown_domain=has_unknown_domain,
        )

    def _detect_type(
        self,
        value: str,
    ) -> str:
        """
        Detecta tipo do QRCode.
        """

        lowered = value.lower()

        if (
            lowered.startswith("http://")
            or lowered.startswith("https://")
        ):
            return "url"

        if "br.gov.bcb.pix" in lowered:
            return "pix"

        return "generic"
