from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class QRCodeData:
    """
    Resultado consolidado da análise
    antifraude do QRCode.
    """

    # valor original
    raw_value: str

    # tipo detectado
    qrcode_type: str

    # validade estrutural
    is_valid: bool

    # score antifraude
    risk_score: int

    # safe | attention | suspicious | fraud_suspect
    status: str

    # explicabilidade
    reasons: list[str]

    positives: list[str]

    # ======================================================
    # PIX
    # ======================================================

    pix_key: Optional[str] = None

    merchant_name: Optional[str] = None

    city: Optional[str] = None

    amount: Optional[float] = None

    txid: Optional[str] = None

    is_valid_crc: Optional[bool] = None

    # ======================================================
    # URL
    # ======================================================

    detected_url: Optional[str] = None

    # ======================================================
    # Segurança
    # ======================================================

    is_suspicious_url: bool = False

    has_unknown_domain: bool = False
