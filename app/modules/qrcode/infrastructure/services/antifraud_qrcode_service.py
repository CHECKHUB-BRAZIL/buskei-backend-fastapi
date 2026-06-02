from app.modules.link_analysis.domain.services.link_analysis_service import (
    LinkAnalysisService,
)
from app.modules.link_analysis.domain.value_objects.url_vo import (
    URLVO,
)

from app.modules.qrcode.domain.exceptions.qrcode_exceptions import (
    InvalidQRCodeException,
)

from app.modules.qrcode.domain.services.qrcode_decoder_service import (
    QRCodeAnalyzerService,
)

from app.modules.qrcode.domain.value_objects.qrcode_data import (
    QRCodeData,
)

from app.modules.qrcode.infrastructure.services.pix_payload_parser import (
    PixPayloadParser,
)


class AntiFraudQRCodeService(QRCodeAnalyzerService):
    """
    Serviço responsável por analisar
    conteúdo de QRCode e executar
    verificações antifraude.
    """

    def __init__(self):
        self._link_analysis_service = (
            LinkAnalysisService()
        )

        self._pix_parser = (
            PixPayloadParser()
        )

    def analyze(
        self,
        content: str,
    ) -> QRCodeData:
        """
        Analisa conteúdo do QRCode.
        """

        if not content:
            raise InvalidQRCodeException()

        raw_value = content.strip()

        qrcode_type = self._detect_type(
            raw_value,
        )

        risk_score = 0

        reasons: list[str] = []

        positives: list[str] = []

        detected_url = None

        is_suspicious_url = False

        has_unknown_domain = False

        pix_key = None

        merchant_name = None

        city = None

        amount = None

        txid = None

        is_valid_crc = None

        # =====================================================
        # URL
        # =====================================================

        if qrcode_type == "url":

            (
                risk_score,
                reasons,
                positives,
            ) = self._analyze_url(
                raw_value,
            )

            detected_url = raw_value

            is_suspicious_url = (
                risk_score >= 50
            )

        # =====================================================
        # PIX
        # =====================================================

        elif qrcode_type == "pix":

            (
                risk_score,
                reasons,
                positives,
            ) = self._analyze_pix(
                raw_value,
            )

            try:

                pix_data = (
                    self._pix_parser.parse(
                        raw_value,
                    )
                )

                pix_key = (
                    pix_data.pix_key
                )

                merchant_name = (
                    pix_data.merchant_name
                )

                amount = (
                    pix_data.amount
                )

                city = (
                    pix_data.city
                )

                txid = (
                    pix_data.txid
                )

                is_valid_crc = (
                    pix_data.is_valid_crc
                )

                if (
                    not pix_data.is_valid_crc
                ):
                    risk_score += 80

                    reasons.append(
                        "Checksum CRC16 do PIX inválido."
                    )

                else:
                    positives.append(
                        "Checksum CRC16 válido."
                    )

                if merchant_name:
                    positives.append(
                        f"Recebedor identificado: {merchant_name}"
                    )

                if city:
                    positives.append(
                        f"Cidade identificada: {city}"
                    )

                if txid:
                    positives.append(
                        f"TXID identificado: {txid}"
                    )

                if amount:
                    positives.append(
                        f"Valor identificado: R$ {amount}"
                    )

            except Exception:

                risk_score += 40

                reasons.append(
                    "Não foi possível interpretar completamente o payload PIX."
                )

        # =====================================================
        # GENERIC
        # =====================================================

        else:

            positives.append(
                "QRCode identificado como conteúdo genérico."
            )

        # =====================================================
        # STATUS
        # =====================================================

        if risk_score >= 80:

            status = "fraud_suspect"

        elif risk_score >= 50:

            status = "suspicious"

        elif risk_score >= 20:

            status = "attention"

        else:

            status = "safe"

        return QRCodeData(
            raw_value=raw_value,
            qrcode_type=qrcode_type,
            is_valid=True,
            risk_score=min(
                risk_score,
                100,
            ),
            status=status,
            reasons=reasons,
            positives=positives,

            # PIX
            pix_key=pix_key,
            merchant_name=merchant_name,
            city=city,
            amount=amount,
            txid=txid,
            is_valid_crc=is_valid_crc,

            # URL
            detected_url=detected_url,

            # Segurança
            is_suspicious_url=is_suspicious_url,
            has_unknown_domain=has_unknown_domain,
        )

    def _analyze_url(
        self,
        url: str,
    ):
        """
        Reutiliza o módulo de análise
        de links já existente.
        """

        url_vo = URLVO(url)

        return (
            self._link_analysis_service.analyze(
                url_vo,
            )
        )

    def _analyze_pix(
        self,
        payload: str,
    ):
        """
        Regras básicas de validação PIX.
        """

        risk_score = 0

        reasons = []

        positives = []

        payload_lower = payload.lower()

        if len(payload) < 30:

            risk_score += 40

            reasons.append(
                "Payload PIX muito curto."
            )

        else:

            positives.append(
                "Payload possui tamanho compatível com PIX."
            )

        if (
            "br.gov.bcb.pix"
            not in payload_lower
        ):

            risk_score += 60

            reasons.append(
                "Payload PIX não segue o padrão BR Code."
            )

        else:

            positives.append(
                "Payload segue o padrão BR Code do Banco Central."
            )

        return (
            risk_score,
            reasons,
            positives,
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
            lowered.startswith(
                "http://"
            )
            or lowered.startswith(
                "https://"
            )
        ):
            return "url"

        if (
            "br.gov.bcb.pix"
            in lowered
        ):
            return "pix"

        return "generic"
