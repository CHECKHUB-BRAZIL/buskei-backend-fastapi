from app.modules.qrcode.application.dto.qrcode_response import (
    QRCodeResponse,
)

from app.modules.qrcode.application.exceptions.qrcode_application_exceptions import (
    QRCodeAnalysisFailedException,
)

from app.modules.qrcode.domain.exceptions.qrcode_exceptions import (
    QRCodeDomainException,
)

from app.modules.qrcode.domain.services.qrcode_decoder_service import (
    QRCodeAnalyzerService,
)


class AnalyzeQRCodeUseCase:
    """
    Use case responsável por:

    - receber conteúdo do QRCode
    - chamar análise antifraude
    - retornar resposta padronizada
    """

    def __init__(
        self,
        analyzer_service: QRCodeAnalyzerService,
    ):
        self._analyzer_service = analyzer_service

    def execute(
        self,
        content: str,
    ) -> QRCodeResponse:
        """
        Executa análise antifraude do QRCode.
        """

        try:
            result = self._analyzer_service.analyze(
                content=content,
            )

            return QRCodeResponse(
                raw_value=result.raw_value,
                qrcode_type=result.qrcode_type,
                is_valid=result.is_valid,
                risk_score=result.risk_score,
                status=result.status,
                reason=result.reason,
                pix_key=result.pix_key,
                merchant_name=result.merchant_name,
                amount=result.amount,
                detected_url=result.detected_url,
                is_suspicious_url=result.is_suspicious_url,
                has_unknown_domain=result.has_unknown_domain,
            )

        # erros do domínio sobem normalmente
        except QRCodeDomainException:
            raise

        # erros inesperados viram erro de application
        except Exception as e:
            raise QRCodeAnalysisFailedException(
                str(e),
            ) from e
